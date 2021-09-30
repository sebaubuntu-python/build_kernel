from build_kernel import get_config, kernel_path, out_path
from build_kernel.utils.device import Device

def print_summary(device: Device):
	print("\n".join([
		"============================================",
		f"PRODUCT_DEVICE={device.PRODUCT_DEVICE}",
		f"TARGET_ARCH={device.TARGET_ARCH}",
		f"TARGET_KERNEL_SOURCE={kernel_path / device.TARGET_KERNEL_SOURCE}",
		f"OUT_DIR={out_path / device.PRODUCT_DEVICE}",
		f"BUILD_USER={get_config('KBUILD_BUILD_USER')}",
		f"BUILD_HOST={get_config('KBUILD_BUILD_HOST')}",
		f"CCACHE={get_config('ENABLE_CCACHE')}",
		"============================================",
	]))
