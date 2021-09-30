"""
Common configuration for msm8998/sdm660 devices
"""

from build_kernel.utils.device import Device

class QcomMSM8998Device(Device):
	TARGET_BUILD_ARTIFACTS = ["Image.gz-dtb"]
