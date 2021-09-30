from device.qcom.sm8150 import QcomSM8150Device

class XiaomiSM8150Device(QcomSM8150Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/sm8150"
