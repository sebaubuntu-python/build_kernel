from build_kernel.utils.device import register_device
from device.lenovo.sdm710 import LenovoSDM710Device

class LenovoKunlun2Device(LenovoSDM710Device):
	PRODUCT_DEVICE = "kunlun2"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(LenovoKunlun2Device)
