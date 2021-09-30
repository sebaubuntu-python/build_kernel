from build_kernel.utils.device import register_device
from device.xiaomi.sdm660 import XiaomiSDM660Device

class XiaomiPlatinaDevice(XiaomiSDM660Device):
	PRODUCT_DEVICE = "platina"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiPlatinaDevice)
