from build_kernel.utils.device import register_device
from device.xiaomi.sm8150 import XiaomiSM8150Device

class XiaomiNabuDevice(XiaomiSM8150Device):
	PRODUCT_DEVICE = "nabu"
	TARGET_KERNEL_FRAGMENTS = ["vendor/xiaomi/sm8150-common.config", f"vendor/xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiNabuDevice)
