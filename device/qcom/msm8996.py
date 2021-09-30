"""
Common configuration for msm8996/msm8937/msm8953 devices
"""

from device.qcom.common import *

# msm8996/msm8937/msm8953 uses 3.18 by default
# but it currently has a 4.9 and 4.19 porting by qcom
# Override as needed
KERNEL_VERSION = "3.18"

# msm8996/msm8937/msm8953 uses v0 boot header
BUILD_ARTIFACTS = ["Image.gz-dtb"]
