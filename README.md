# build_kernel

[![PyPi version](https://img.shields.io/pypi/v/build_kernel)](https://pypi.org/project/build_kernel/)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/83567b747b614dc7892e1c2c1bf8cbd9)](https://www.codacy.com/gh/SebaUbuntu/android-kernel-builder/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/android-kernel-builder&amp;utm_campaign=Badge_Grade)

Little build system to build Linux

-   Clones AOSP Clang automatically
-   Managed with config files
-   Automatic AnyKernel3 packing

Requires Python 3.8 or greater

## Installation

```sh
pip3 install build_kernel
```

## Sources preparation

-   Add a config for your kernel in `device/vendor/codename.py` (check the example config in `device/examples/example.py`)
-   Add kernel sources in `kernel/` (in the path that you specified in the config)

## Instructions

```sh
python3 -m build_kernel
```

## License

```
#
# Copyright (C) 2022 Sebastiano Barezzi
#
# SPDX-License-Identifier: LGPL-3.0-or-later
#
```
