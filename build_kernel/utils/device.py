from build_kernel.utils.logging import LOGE, format_exception
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules
from typing import Dict, List, Optional

class Device:
	PRODUCT_DEVICE: str

	TARGET_ARCH: str
	TARGET_KERNEL_CONFIG: str
	TARGET_KERNEL_FRAGMENTS: List[str] = []
	TARGET_KERNEL_SOURCE: Path

	AB_OTA_UPDATER: bool = False
	BOARD_BUILD_SYSTEM_ROOT_IMAGE: bool = False
	TARGET_BLOCK_DEVICE: str = "/dev/block/bootdevice/by-name/boot"

	BOARD_KERNEL_IMAGE_NAME: str
	BOARD_INCLUDE_DTB_IN_BOOTIMG: bool = False
	BOARD_KERNEL_SEPARATED_DTBO: bool = False
	BOARD_KERNEL_PAGESIZE: int = 2048

	TARGET_ADDITIONAL_MAKE_FLAGS: List[str] = []
	TARGET_KERNEL_USE_HOST_COMPILER: bool = False
	TARGET_KERNEL_CROSS_COMPILE_PREFIX: Optional[str] = None
	TARGET_KERNEL_CLANG_COMPILE: bool = True
	TARGET_KERNEL_GCC_VERSION: Optional[str] = None
	TARGET_KERNEL_CLANG_VERSION: Optional[str] = None

devices: Dict[str, Device] = {}

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
