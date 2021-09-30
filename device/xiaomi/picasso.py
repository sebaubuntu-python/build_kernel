from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiPicassoDevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "picasso"
	TARGET_KERNEL_CONFIG = f"vendor/{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiPicassoDevice)
