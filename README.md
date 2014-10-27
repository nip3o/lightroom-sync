lightroom-sync
==============

Script for migrating Adobe Lightroom catalogs between different computers, where the same files are located on different system paths.

## Intended setup
Each computer has its own Lightroom catalog, stored and synced using Dropbox or similar. The script takes the most recent Lightroom catalog and creates copies of it that can be used on the other hosts.

## Installation
1. Clone repo and install dependencies.
2. Specify your catalogs in a file named `catalogs.conf`. There is a sample file in the repo to help ypu get started.

## Usage
Simply run `lrsync.py`.
