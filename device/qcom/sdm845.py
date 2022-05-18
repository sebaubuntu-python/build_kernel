"""Common configuration for sdm845/sdm710 devices."""

from build_kernel.utils.device import Device

class QcomSDM845Device(Device):
	BOARD_KERNEL_IMAGE_NAME = "Image.gz-dtb"
	BOARD_KERNEL_SEPARATED_DTBO = True
