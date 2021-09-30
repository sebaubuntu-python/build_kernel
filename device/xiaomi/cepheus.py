from build_kernel.utils.device import register_device
from device.xiaomi.sm8150 import XiaomiSM8150Device

class XiaomiCepheusDevice(XiaomiSM8150Device):
	PRODUCT_DEVICE = "cepheus"
	TARGET_KERNEL_CONFIG = f"vendor/{PRODUCT_DEVICE}_defconfig"
	BOARD_BUILD_SYSTEM_ROOT_IMAGE = True

register_device(XiaomiCepheusDevice)
