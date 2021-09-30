"""
Common configuration for msm8996/msm8937/msm8953 devices
"""

from build_kernel.utils.device import Device

class QcomMSM8996Device(Device):
	TARGET_BUILD_ARTIFACTS = ["Image.gz-dtb"]
