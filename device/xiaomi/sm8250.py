from device.qcom.sm8250 import QcomSM8250Device

class XiaomiSM8250Device(QcomSM8250Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/sm8250"
