# TabbyVision
 TabbyVision: a lightweight Python script for data visualization from the command line. Gain valuable insights from your data.

## Requirements

You'll need Python 3.10.8 or greater to run TabbyVision.py

* [xlrd](https://pypi.org/project/xlrd/) >= 2.0.1
> pip install xlrd
* [prettytable](https://pypi.org/project/prettytable/) >= 3.6.0
> pip install prettytable

## Installation

```bash
git clone https://github.com/AvirFrog/TabbyVision

python TabbyVision.py --help
```

## Input data

This code expects a file containing tabular data in one of the following formats: CSV, TSV, XLS, or XLSX. The file should have a header row containing the column names, and each subsequent row should contain the data for one record.

## Quick usage

```bash
python TabbyVision.py data.csv
```

This will output tabel from PrettyTable

```bash
+-----------+------+------------+-----------------+
| City name | Area | Population | Annual Rainfall |
+-----------+------+------------+-----------------+
| Adelaide  | 1295 |  1158259   |      600.5      |
| Brisbane  | 5905 |  1857594   |      1146.4     |
| Darwin    | 112  |   120900   |      1714.7     |
| Hobart    | 1357 |   205556   |      619.5      |
| Melbourne | 1566 |  3806092   |      646.9      |
| Perth     | 5386 |  1554769   |      869.4      |
| Sydney    | 2058 |  4336374   |      1214.8     |
+-----------+------+------------+-----------------+
```

## Full usage

```txt
usage: TabbyVision.py [-h] [-o OUTPUT] [-c column old new] [-n] [-d] [-l]
                      filename

Simple table manipulator. Version 1.0 by Kacper Dudczak

positional arguments:
  filename              path to the input file

options:
  -h, --help            show this help message and exit
  -o, --output          OUTPUT
                        path to the output file
  -c, --change          column old new
                        change values in the column
  -n, --nan             replace NaN or empty places with mean value
  -d, --dimensions      display table dimensions
  -l, --list-columns    display list of columns in the table
```

## License

[GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html)