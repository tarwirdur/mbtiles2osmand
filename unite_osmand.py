#!/usr/bin/env python3
import io
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser(description='Unite multiple osmand files into single')

parser.add_argument('input', nargs='+', help='input files. If multiple files contain tile with the same coordinates, tile from first (from argument list file will be used')
parser.add_argument('output', help='output file')
parser.add_argument('-f', '-force', action='store_true', help='override output file if exists')
args = parser.parse_args()

if os.path.isfile(args.output):
    if args.f:
        os.remove(args.output)
    else:
        print("Output file already exists. Add -f option for overwrite")
        exit(1)


dest = sqlite3.connect(args.output)
dcur = dest.cursor()
dcur.execute('''CREATE TABLE tiles (x int, y int, z int, s int, image blob, PRIMARY KEY (x,y,z,s));''')
dcur.execute('''CREATE TABLE info (maxzoom Int, minzoom Int);''')

for source_file in args.input:
    source = sqlite3.connect(source_file)
    scur = source.cursor()
    for row in scur.execute("SELECT z, x, y, image FROM tiles"):
        image = row[3]
        z, x, y, s = int(row[0]), int(row[1]), int(row[2]), 0
        dcur.execute("select count(*) from tiles where x=? and y=? and z=?", [x,y,z])
        if dcur.fetchone()[0] == 0:
            dcur.execute("INSERT INTO tiles (x, y, z, s, image) VALUES (?, ?, ?, ?, ?)", [x, y, z, s, sqlite3.Binary(image)])
    source.close()

dcur.execute("INSERT INTO info (maxzoom, minzoom) SELECT max(z),min(z) from tiles")

dest.commit()
dest.close()

