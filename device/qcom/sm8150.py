"""Common configuration for sm8150/sm6150/sm6250 devices."""

from build_kernel.utils.device import Device

class QcomSM8150Device(Device):
	BOARD_KERNEL_IMAGE_NAME = "Image"
	BOARD_INCLUDE_DTB_IN_BOOTIMG = True
	BOARD_KERNEL_SEPARATED_DTBO = True
