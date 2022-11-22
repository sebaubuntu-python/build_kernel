from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiElishDevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "elish"
	TARGET_KERNEL_FRAGMENTS = ["vendor/xiaomi/sm8250-common.config", f"vendor/xiaomi/{PRODUCT_DEVICE}.config"]
	AB_OTA_UPDATER = True

register_device(XiaomiElishDevice)
