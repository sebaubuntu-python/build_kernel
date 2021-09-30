"""
Common configuration for sm8150/sm6150/sm6250 devices
"""

from build_kernel.utils.device import Device

class QcomSM8150Device(Device):
	TARGET_BUILD_ARTIFACTS = ["Image", "dtb.img", "dtbo.img"]
