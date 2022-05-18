from build_kernel.utils.device import Device, register_device

class MsftTalkmanDevice(Device):
	PRODUCT_DEVICE = "talkman"
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"
	TARGET_KERNEL_SOURCE = "kernel/msft/talkman"
	TARGET_BLOCK_DEVICE = "/dev/block/by-name/boot"
	BOARD_KERNEL_IMAGE_NAME = "Image.gz"
	TARGET_KERNEL_USE_HOST_COMPILER = True
	TARGET_KERNEL_CROSS_COMPILE_PREFIX = "aarch64-linux-gnu-"

register_device(MsftTalkmanDevice)
