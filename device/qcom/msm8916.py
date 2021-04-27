"""
Common configuration for msm8916 devices
"""

from device.qcom.common import *

# msm8916 uses 3.10 by default
KERNEL_VERSION = "3.10"

# msm8916 uses v0 boot header
BUILD_ARTIFACTS = ["zImage", "dt.img"]

# Cross-compiler (gcc or clHAHAHAHAHAHAHA)
TOOLCHAIN = "gcc"
