# package-fs-info
Find file that are not owned by a package in the filesystem.

## Purpose

You're using `pacman` as to maintain your packages and you want to know what files are not managed by any package.

## Features
usage: `package-fs-info.py [-h] [--load FILENAME] [--save FILENAME] [--orphant-files] [--nonexisting-files] [--stats]`

optional arguments:
  - `-h`, `--help`         show this help message and exit
  - `--load FILENAME`      Load a previously saved database from `FILENAME`.
  - `--save FILENAME`      Save the database into `FILENAME` for later usage.
  - `--orphant-files`      Print files that are not owned by a package.
  - `--nonexisting-files`  Print files that belong to a package but don't exist in the file system.
  - `--stats`              Print general information and statistics.
