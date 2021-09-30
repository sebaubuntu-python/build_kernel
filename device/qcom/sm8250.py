"""
Common configuration for sm8250 devices
"""

from device.qcom.common import *

# sm8250 uses 4.19
KERNEL_VERSION = "4.19"

# sm8250 uses v2 boot header
BUILD_ARTIFACTS = ["Image", "dtb.img", "dtbo.img"]
