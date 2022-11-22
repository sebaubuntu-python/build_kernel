from build_kernel.utils.device import register_device
from device.xiaomi.sdm660 import XiaomiSDM660Device

class XiaomiWhyredDevice(XiaomiSDM660Device):
	PRODUCT_DEVICE = "whyred"
	TARGET_KERNEL_FRAGMENTS = [f"vendor/xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiWhyredDevice)
