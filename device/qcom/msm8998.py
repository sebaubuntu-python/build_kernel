"""Common configuration for msm8998/sdm660 devices."""

from build_kernel.utils.device import Device

class QcomMSM8998Device(Device):
	BOARD_KERNEL_IMAGE_NAME = "Image.gz-dtb"
