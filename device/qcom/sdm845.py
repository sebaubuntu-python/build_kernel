"""
Common configuration for sdm845/sdm710 devices
"""

from device.qcom.common import *

# sdm845/sdm710 uses 4.9
KERNEL_VERSION = "4.9"

# sdm845/sdm710 uses v1 boot header
BUILD_ARTIFACTS = ["Image.gz-dtb", "dtbo.img"]

# Cross-compiler (gcc or clang)
TOOLCHAIN = "clang"
