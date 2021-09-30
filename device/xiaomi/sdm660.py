from device.qcom.msm8998 import QcomMSM8998Device

class XiaomiSDM660Device(QcomMSM8998Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/sdm660"
