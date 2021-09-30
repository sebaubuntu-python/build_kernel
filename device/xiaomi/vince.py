from build_kernel.utils.device import register_device
from device.xiaomi.msm8953 import XiaomiMSM8953Device

class XiaomiVinceDevice(XiaomiMSM8953Device):
	PRODUCT_DEVICE = "vince"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiVinceDevice)
