from build_kernel.utils.device import register_device
from device.asus.msm8937 import AsusMSM8937Device

class AsusX00RDevice(AsusMSM8937Device):
	PRODUCT_DEVICE = "X00R"
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"

register_device(AsusX00RDevice)
