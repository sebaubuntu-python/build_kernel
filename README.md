# Android kernel building script

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/83567b747b614dc7892e1c2c1bf8cbd9)](https://www.codacy.com/gh/SebaUbuntu/android-kernel-builder/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/android-kernel-builder&amp;utm_campaign=Badge_Grade)

Little build system to build Android kernel sources

-   Clones AOSP Clang automatically
-   Managed with config files
-   Automatic AnyKernel3 packing

Note: Requires Python 3.9

## Installation

-   Clone the repo
-   Open a terminal with pwd as the cloned repo
-   `pip3 install .`

## Sources preparation

-   Add a config for your kernel in `device/vendor/codename.py` (check the example config in `device/examples/example.py`)
-   Add kernel sources in `kernel/` (in the path that you specified in the config)

## How to use

```sh
$ python3 -m build_kernel -h
usage: python3 -m kernel_build [-h] [-c] [-v] device

positional arguments:
  device         device codename

optional arguments:
  -h, --help     show this help message and exit
  -c, --clean    clean before building
  -v, --verbose  verbose logging
```
