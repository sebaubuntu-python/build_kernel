from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiThymeDevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "thyme"
	TARGET_KERNEL_CONFIG = f"vendor/{PRODUCT_DEVICE}_defconfig"
	AB_OTA_UPDATER = True

register_device(XiaomiThymeDevice)
