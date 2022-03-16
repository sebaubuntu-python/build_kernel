from build_kernel.utils.device import register_device
from device.xiaomi.sdm710 import XiaomiSDM710Device

class XiaomiGrusDevice(XiaomiSDM710Device):
	PRODUCT_DEVICE = "grus"
	TARGET_KERNEL_FRAGMENTS = ["xiaomi/sdm710-common.config", f"xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiGrusDevice)
