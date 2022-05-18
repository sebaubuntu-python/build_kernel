from build_kernel.utils.device import Device, register_device

class GoogleMainlineGkix8664Device(Device):
	PRODUCT_DEVICE = "mainline_gki_x86_64"
	TARGET_ARCH = "x86_64"
	TARGET_KERNEL_CONFIG = "gki_defconfig"
	TARGET_KERNEL_SOURCE = "kernel/google/android-mainline"
	TARGET_BLOCK_DEVICE = "/dev/block/by-name/boot"
	BOARD_KERNEL_IMAGE_NAME = "vmlinuz"
	TARGET_KERNEL_USE_HOST_COMPILER = True

register_device(GoogleMainlineGkix8664Device)
