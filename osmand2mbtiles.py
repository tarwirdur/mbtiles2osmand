#!/usr/bin/env python3
import io
import sqlite3
import argparse
import os

parser = argparse.ArgumentParser(description='Converts osmand tile format to mbtiles format')

parser.add_argument('input', help='input file')
parser.add_argument('output', help='output file')
parser.add_argument('-f', '-force', action='store_true', help='override output file if exists')
args = parser.parse_args()

if os.path.isfile(args.output):
    if args.f:
        os.remove(args.output)
    else:
        print("Output file already exists. Add -f option for overwrite")
        exit(1)


source = sqlite3.connect(args.input)
dest = sqlite3.connect(args.output)

scur = source.cursor()
dcur = dest.cursor()

dcur.execute('''CREATE TABLE tiles (zoom_level int, tile_column int, tile_row int, tile_data blob, PRIMARY KEY (zoom_level, tile_column, tile_row));''')
dcur.execute('''CREATE TABLE metadata (name text, value text);''')

fmt=''

for row in scur.execute("SELECT z, x, y, image FROM tiles"):
    image = row[3]
    z, x, y = int(row[0]), int(row[1]), int(row[2])
    z = 17 - z
    y = 2 ** z - 1 - y
    dcur.execute("INSERT INTO tiles (tile_column, tile_row, zoom_level, tile_data) VALUES (?, ?, ?, ?)", [x, y, z, sqlite3.Binary(image)])
    if fmt == '':
        if image[0:3] == b'\xff\xd8\xff':
            fmt = 'jpg'
        if image[0:8] == b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a':
            fmt = 'png'


dcur.execute("INSERT INTO metadata (name, value) VALUES ('name', ?)", ['layerName']);
dcur.execute("INSERT INTO metadata (name, value) VALUES ('type', 'baselayer')");
dcur.execute("INSERT INTO metadata (name, value) VALUES ('version', '1')");
dcur.execute("INSERT INTO metadata (name, value) VALUES ('format', ?)", [fmt]);
dcur.execute("INSERT INTO metadata (name, value) VALUES ('description', '')");

dest.commit()
source.close()
dest.close()

