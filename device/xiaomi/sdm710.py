from device.qcom.sdm845 import QcomSDM845Device

class XiaomiSDM710Device(QcomSDM845Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/sdm710"
	TARGET_KERNEL_CONFIG = "sdm670-perf_defconfig"
	BOARD_KERNEL_IMAGE_NAME = "Image"
	BOARD_INCLUDE_DTB_IN_BOOTIMG = True
	BOARD_KERNEL_SEPARATED_DTBO = True
