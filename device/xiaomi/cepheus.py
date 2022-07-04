from build_kernel.utils.device import register_device
from device.xiaomi.sm8150 import XiaomiSM8150Device

class XiaomiCepheusDevice(XiaomiSM8150Device):
	PRODUCT_DEVICE = "cepheus"
	TARGET_KERNEL_FRAGMENTS = ["vendor/xiaomi/sm8150-common.config", f"vendor/xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiCepheusDevice)
