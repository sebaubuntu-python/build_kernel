from device.qcom.msm8996 import QcomMSM8996Device

class AsusMSM8937Device(QcomMSM8996Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/asus/msm8937"
	BOARD_BUILD_SYSTEM_ROOT_IMAGE = True
