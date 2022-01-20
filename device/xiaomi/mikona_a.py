from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiMikonaADevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "mikona_a"
	TARGET_KERNEL_CONFIG = f"vendor/mikona_defconfig"

register_device(XiaomiMikonaADevice)
