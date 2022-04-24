from build_kernel.utils.device import register_device
from device.xiaomi.sm8250 import XiaomiSM8250Device

class XiaomiMikonaVabDevice(XiaomiSM8250Device):
	PRODUCT_DEVICE = "mikona_vab"
	TARGET_KERNEL_CONFIG = "vendor/mikona_defconfig"
	AB_OTA_UPDATER = True

register_device(XiaomiMikonaVabDevice)
