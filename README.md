Converts mbtiles format to sqlitedb format suitable for OsmAnd and RMaps.
Also possible convert tiles to jpeg to reduce the file size (`--jpg` option).

# Usage

`python3 mbtiles2osmand.py [-h] [-f] [--jpg JPEG_QUALITY] input output`

```
input               input file
output              output file

optional arguments:
  -h, --help          show this help message and exit
  -f, -force          override output file if exists
  --jpg JPEG_QUALITY  convert tiles to JPEG with specified quality
```

# Examples

Simple:
`python3 mbtiles2osmand.py input.mbtiles output.sqlitedb`

Converting tiles to jpeg with compression:
`python3 mbtiles2osmand.py --jpg 75 input.mbtiles output.sqlitedb`

___

# unite_osmand

`python3 unite_osmand.py [-h] [-f] input [input ...] output`

```
Unite multiple osmand files into single

positional arguments:
  input       input files. If multiple files contain tile with the same coordinates, tile from first (from argument list file will be used
  output      output file

optional arguments:
  -h, --help  show this help message and exit
  -f, -force  override output file if exists
```
