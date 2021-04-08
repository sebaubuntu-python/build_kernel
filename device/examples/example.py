# Note: if the kernel sources supports multiple devices,
# it's suggested to create a commonized config file and source it on the device-specific config
#from device.examples.common import *

# Device info
CODENAME = "example"
DEFCONFIG = f"{CODENAME}_defconfig"

# Device info
ARCH = "arm64"
# False: A-only, else True
IS_AB = False
# True: It has a ramdisk in boot.img, else False
HAS_RAMDISK = False
DEVICE_BLOCK_PARTITION = "/dev/block/bootdevice/by-name/boot"

# Kernel sources folder name
# Kernel sources, in this case, must be in kernels/example
KERNEL_PATH = "example"

# Building artifacts list (e.g. ["Image", "dtb.img"], or ["Image.gz-dtb"])
BUILD_ARTIFACTS = ["Image.gz-dtb"]

# Cross-compiler (gcc or clang)
TOOLCHAIN = "clang"
