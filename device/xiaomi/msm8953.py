from device.qcom.msm8996 import QcomMSM8996Device

class XiaomiMSM8953Device(QcomMSM8996Device):
	TARGET_ARCH = "arm64"
	TARGET_KERNEL_SOURCE = "kernel/xiaomi/msm8953"
