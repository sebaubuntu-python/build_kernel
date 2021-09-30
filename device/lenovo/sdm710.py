from device.qcom.sdm845 import QcomSDM845Device

class LenovoSDM710Device(QcomSDM845Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/lenovo/sdm710"
	BOARD_BUILD_SYSTEM_ROOT_IMAGE = False
