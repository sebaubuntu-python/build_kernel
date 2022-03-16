from build_kernel.utils.device import register_device
from device.xiaomi.sdm710 import XiaomiSDM710Device

class XiaomiSiriusDevice(XiaomiSDM710Device):
	PRODUCT_DEVICE = "sirius"
	TARGET_KERNEL_FRAGMENTS = ["xiaomi/sdm710-common.config", f"xiaomi/{PRODUCT_DEVICE}.config"]

register_device(XiaomiSiriusDevice)
