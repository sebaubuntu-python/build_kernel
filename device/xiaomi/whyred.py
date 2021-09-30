from build_kernel.utils.device import register_device
from device.xiaomi.sdm660 import XiaomiSDM660Device

class XiaomiWhyredDevice(XiaomiSDM660Device):
	PRODUCT_DEVICE = "whyred"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiWhyredDevice)
