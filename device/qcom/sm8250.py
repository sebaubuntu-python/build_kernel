"""
Common configuration for sm8250/sm7250 devices
"""

from build_kernel.utils.device import Device

class QcomSM8250Device(Device):
	TARGET_BUILD_ARTIFACTS = ["Image", "dtb.img", "dtbo.img"]
