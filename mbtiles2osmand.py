#!/usr/bin/env python3
import io
import sqlite3
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description='Converts mbtiles format to sqlitedb format suitable for OsmAnd')

parser.add_argument('input', help='input file')
parser.add_argument('output', help='output file')
parser.add_argument('-f', '-force', action='store_true', help='override output file if exists')
parser.add_argument('--jpg', dest='jpeg_quality', action='store', help='convert tiles to JPEG with specified quality')
args = parser.parse_args()

if os.path.isfile(args.output):
    if args.f:
        os.remove(args.output)
    else:
        print("Output file already exists. Add -f option for overwrite")
        exit(1)


# See:
# * https://github.com/osmandapp/Osmand/blob/master/OsmAnd/src/net/osmand/plus/SQLiteTileSource.java


def to_jpg(raw_bytes, quality):
    im = Image.open(io.BytesIO(raw_bytes))
    im = im.convert('RGB')
    stream = io.BytesIO()
    im.save(stream, format = "JPEG", subsampling=0, quality=quality)
    return stream.getvalue()

source = sqlite3.connect(args.input)
dest = sqlite3.connect(args.output)


scur = source.cursor()
dcur = dest.cursor()

dcur.execute('''CREATE TABLE tiles (x int, y int, z int, s int, image blob, PRIMARY KEY (x,y,z,s));''')
dcur.execute('''CREATE TABLE info (maxzoom Int, minzoom Int);''')

for row in scur.execute("SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles"):
    image = row[3]
    if(args.jpeg_quality != None):
        image = to_jpg(image, int(args.jpeg_quality))
    z, x, y, s = int(row[0]), int(row[1]), int(row[2]), 0
    y = 2 ** z - 1 - y
    z = 17 - z
    dcur.execute("INSERT INTO tiles (x, y, z, s, image) VALUES (?, ?, ?, ?, ?)", [x, y, z, s, sqlite3.Binary(image)])

dcur.execute("INSERT INTO info (maxzoom, minzoom) SELECT max(z),min(z) from tiles")

dest.commit()
source.close()
dest.close()

