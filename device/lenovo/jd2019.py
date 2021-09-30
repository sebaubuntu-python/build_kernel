from build_kernel.utils.device import register_device
from device.lenovo.sdm710 import LenovoSDM710Device

class LenovoJd2019Device(LenovoSDM710Device):
	PRODUCT_DEVICE = "jd2019"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(LenovoJd2019Device)
