# Android kernel building script

Little build system to build Android kernel sources

- Clones AOSP Clang automatically
- Managed with config files
- Automatic AnyKernel3 packing

Note: Requires Python 3.9 and the filesize is about 500MB+

## Installation

- Clone the repo
- Open a terminal with pwd as the cloned repo
- `pip3 install .`

## Sources preparation

- Add a config for your kernel in `device/vendor/codename.py` (check the example config in `device/examples/example.py`)
- Add kernel sources in `kernel/` (in the path that you specified in the config)

## How to use

```
$ python3 -m build_kernel -h
usage: python3 -m kernel_build [-h] [-c] [-v] device

positional arguments:
  device         device codename

optional arguments:
  -h, --help     show this help message and exit
  -c, --clean    clean before building
  -v, --verbose  verbose logging
```
