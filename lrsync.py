# -*- coding: utf-8 -*-
import os
import time
import shutil
import ConfigParser

from collections import namedtuple

from pony.orm import Database, PrimaryKey, Required, db_session


class Catalog(namedtuple('Catalog', ['name', 'path', 'root_folder'])):
    @property
    def modification_date(self):
        return time.ctime(os.path.getmtime(self.path))


def update_database(db_path, root_folder):
    db = Database('sqlite', db_path, create_db=False)

    class AgLibraryRootFolder(db.Entity):
        id_local = PrimaryKey(int, auto=True)
        absolutePath = Required(str)

    db.generate_mapping(create_tables=False)

    with db_session:
        folder = AgLibraryRootFolder.get()
        folder.absolutePath = root_folder


def main():
    catalogs = set()

    config = ConfigParser.RawConfigParser()
    config.read('catalogs.conf')

    for section in config.sections():
        catalog = Catalog(
            name=section,
            path=config.get(section, 'path'),
            root_folder=config.get(section, 'root_folder')
        )
        catalogs.add(catalog)

    latest_catalog = max(catalogs, key=lambda h: h.modification_date)
    old_catalogs = catalogs.difference({latest_catalog})

    print 'Most recent catalog is %s (%s)' % (latest_catalog.name, latest_catalog.modification_date)

    for catalog in old_catalogs:
        print 'Updating catalog %s...' % catalog.name,
        shutil.copy(latest_catalog.path, catalog.path)
        update_database(db_path=catalog.path, root_folder=catalog.root_folder)
        print 'done'


if __name__ == '__main__':
    main()
