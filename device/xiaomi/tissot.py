from build_kernel.utils.device import register_device
from device.xiaomi.msm8953 import XiaomiMSM8953Device

class XiaomiTissotDevice(XiaomiMSM8953Device):
	PRODUCT_DEVICE = "tissot"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"
	AB_OTA_UPDATER = True
	BOARD_BUILD_SYSTEM_ROOT_IMAGE = True

register_device(XiaomiTissotDevice)
