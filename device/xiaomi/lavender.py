from build_kernel.utils.device import register_device
from device.xiaomi.sdm660 import XiaomiSDM660Device

class XiaomiLavenderDevice(XiaomiSDM660Device):
	PRODUCT_DEVICE = "lavender"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiLavenderDevice)
