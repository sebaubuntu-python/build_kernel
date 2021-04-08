"""
Common configuration for msm8998/sdm660 devices
"""

from device.qcom.common import *

# msm8998/sdm660 uses 4.4 by default
# but it currently has a 4.14 and 4.19 porting by qcom
# Override as needed
KERNEL_VERSION = "4.4"

# msm8998/sdm660 uses v0 boot header
BUILD_ARTIFACTS = ["Image.gz-dtb"]

# Cross-compiler (gcc or clang)
TOOLCHAIN = "clang"
