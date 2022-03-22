from build_kernel.utils.device import Device, register_device

class MsftTalkmanDevice(Device):
	PRODUCT_DEVICE = "talkman"
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"
	TARGET_KERNEL_SOURCE = "kernel/msft/talkman"
	TARGET_BLOCK_DEVICE = "/dev/block/by-name/boot"
	TARGET_BUILD_ARTIFACTS = ["Image.gz"]

register_device(MsftTalkmanDevice)
