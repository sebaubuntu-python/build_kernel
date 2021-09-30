from build_kernel.utils.device import register_device
from device.xiaomi.msm8953 import XiaomiMSM8953Device

class XiaomiMidoDevice(XiaomiMSM8953Device):
	PRODUCT_DEVICE = "mido"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(XiaomiMidoDevice)
