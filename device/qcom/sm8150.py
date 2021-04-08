"""
Common configuration for sm8150/sm6150/sm6250 devices
"""

from device.qcom.common import *

# sm8150/sm6150/sm6250 uses 4.14
KERNEL_VERSION = "4.14"

# sm8150/sm6150/sm6250 uses v2 boot header
BUILD_ARTIFACTS = ["Image", "dtb.img", "dtbo.img"]

# Cross-compiler (gcc or clang)
TOOLCHAIN = "clang"
