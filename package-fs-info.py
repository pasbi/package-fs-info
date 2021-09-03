#!/usr/bin/env python3


import argparse
import json
import subprocess

def increment(the_map, key, zero=0, increment=1):
    the_map[key] = the_map.get(key, zero) + increment

def find_installed_packages():
    pc = subprocess.run(['pacman', '-Q'], capture_output=True)
    return [l.split()[0].decode('utf-8') for l in pc.stdout.splitlines()]

def find_files_of_package(package_name):
    pc = subprocess.run(['pacman', '-Ql', package_name], capture_output=True)
    return [l.split(maxsplit=1)[1].decode('utf-8') for l in pc.stdout.splitlines()]

def find_files(roots):
    pc = subprocess.run(['find'] + roots, capture_output=True)
    return [l.decode('utf-8') for l in pc.stdout.splitlines()]

def build_database():
    print("Retrieving system file list ...", end='')
    files = find_files(['/usr', '/var', '/etc', '/opt'])
    print(f" {len(files)} files.")
    packages_by_file = {fn: ['.'] for fn in files}
    packages = find_installed_packages()
    n = len(packages)
    for i, package in enumerate(packages):
        print(f"Analyzing package ({i}/{n}) {package:40s}.", end='\r')
        for file in find_files_of_package(package):
            if file.endswith('/'):
                file = file[:-1]
            increment(packages_by_file, file, [], [package])
    print("")
    return packages_by_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--load', default=None)
    parser.add_argument('--save', default=None)
    parser.add_argument('--orphant-files', action='store_true')
    parser.add_argument('--nonexisting-files', action='store_true')
    parser.add_argument('--stats', action='store_true')
    args = parser.parse_args()

    if args.load:
        with open(args.load) as f:
            packages_by_file = json.load(f)
    else:
        packages_by_file = build_database()

    if args.save:
        with open(args.save, 'w') as f:
            json.dump(packages_by_file, f)

    if args.orphant_files:
        files = [f for f, p in packages_by_file.items() if p == ['.']]
        print(f"Files that don't belong to an package: ({len(files)})")
        for f in files:
            print(f)

    if args.nonexisting_files:
        files = {f: p for f, p in packages_by_file.items() if '.' not in p}
        print(f"Files that don't exist in the filesystem but belong to a package: ({len(files)})")
        for f, p in files.items():
            print(f, p)

    if args.stats:
        print(f"Number of analyzed files: {len(packages_by_file)}")
        counter = {}
        for f, p in packages_by_file.items():
            increment(counter, len(p), 0, 1)
        for count in sorted(counter.keys()):
            n = counter[count]
            print(f"{n} files are owned by {count-1} packages")
                
