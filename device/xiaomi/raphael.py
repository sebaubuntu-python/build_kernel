from build_kernel.utils.device import register_device
from device.xiaomi.sm8150 import XiaomiSM8150Device

class XiaomiRaphaelDevice(XiaomiSM8150Device):
	PRODUCT_DEVICE = "raphael"
	TARGET_KERNEL_FRAGMENTS = ["vendor/xiaomi/sm8150-common.config", f"vendor/xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiRaphaelDevice)
