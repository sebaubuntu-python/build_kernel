"""
Common configuration for sdm845/sdm710 devices
"""

from build_kernel.utils.device import Device

class QcomSDM845Device(Device):
	TARGET_BUILD_ARTIFACTS = ["Image.gz-dtb", "dtbo.img"]
