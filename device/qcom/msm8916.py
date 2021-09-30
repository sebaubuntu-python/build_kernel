"""
Common configuration for msm8916 devices
"""

from build_kernel.utils.device import Device

class QcomMSM8916Device(Device):
	TARGET_BUILD_ARTIFACTS = ["zImage", "dt.img"]
