# Android kernel building script

## Little build system to build Android kernel sources

- Includes GCC and Clang support
- Managed with config files
- Automatic AnyKernel3 packing

## Instructions

- Add a config for your kernel in `device/vendor/codename.py` (check the example config in device/examples/example.py)
- Add kernel sources in `kernel/`
- `python3 -m build_kernel vendor/codename [-c]`

Arguments:

    config - name of the config to use

    -c or --clean - do make clean before building
