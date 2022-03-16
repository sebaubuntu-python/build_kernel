from device.qcom.sdm845 import QcomSDM845Device

class XiaomiSDM710Device(QcomSDM845Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/sdm710"
	TARGET_KERNEL_CONFIG = "sdm670-perf_defconfig"
	TARGET_BUILD_ARTIFACTS = ["Image", "dtb.img", "dtbo.img"]
