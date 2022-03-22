from build_kernel import kernel_path, out_path
from build_kernel.utils.device import Device
from build_kernel.utils.make import KBUILD_BUILD_USER, KBUILD_BUILD_HOST, ENABLE_CCACHE

def dumpvars(device: Device):
	vars = {
		"PRODUCT_DEVICE": device.PRODUCT_DEVICE,
		"TARGET_ARCH": device.TARGET_ARCH,
		"TARGET_KERNEL_SOURCE": kernel_path / device.TARGET_KERNEL_SOURCE,
		"OUT_DIR": out_path / device.PRODUCT_DEVICE,
		"BUILD_USER": KBUILD_BUILD_USER,
		"BUILD_HOST": KBUILD_BUILD_HOST,
		"CCACHE": ENABLE_CCACHE,
	}

	print("\n".join([
		"============================================",
		*[f"{k}={v}" for k, v in vars.items()],
		"============================================",
	]))
