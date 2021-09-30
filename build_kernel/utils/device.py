from build_kernel.utils.logging import LOGE, LOGI, format_exception
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

class Device:
	PRODUCT_DEVICE: str
	TARGET_ARCH: str
	TARGET_KERNEL_CONFIG: str
	TARGET_KERNEL_SOURCE: Path
	AB_OTA_UPDATER: bool = False
	BOARD_BUILD_SYSTEM_ROOT_IMAGE: bool = False
	TARGET_BLOCK_DEVICE: str = "/dev/block/bootdevice/by-name/boot"
	TARGET_BUILD_ARTIFACTS: list[str] = []
	TARGET_ADDITIONAL_MAKE_FLAGS: list[str] = []

devices: dict[str, Device] = {}

def register_device(device: Device):
	devices[device.PRODUCT_DEVICE] = device

def register_devices(device_path: Path):
	"""Import all the sections and let them execute register_section()."""
	for vendor_name in [folder.name for folder in device_path.iterdir() if folder.is_dir()]:
		for device_name in [name for _, name, _ in iter_modules([str(device_path / vendor_name)])]:
			try:
				import_module(f'device.{vendor_name}.{device_name}')
			except Exception as e:
				LOGE(f"Error importing device {vendor_name}/{device_name}:\n"
					f"{format_exception(e)}")
