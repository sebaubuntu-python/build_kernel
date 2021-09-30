from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiCmiDevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "cmi"
	TARGET_KERNEL_CONFIG = f"vendor/{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiCmiDevice)
