from build_kernel import out_path
from build_kernel.utils.config import get_config
from build_kernel.utils.device import Device
from build_kernel.utils.logging import LOGI
from build_kernel.utils.make import KERNEL_NAME, KERNEL_VERSION
from datetime import date
from git import Repo
from pathlib import Path
from shutil import copyfile, rmtree, make_archive
from stat import S_IWRITE

ANYKERNEL3_REMOTE = "https://github.com/osm0sis/AnyKernel3"

AK3_CONFIG = """\
# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers
## AnyKernel setup
# begin properties
properties() {{ '
kernel.string={kernel_name}
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1={device.PRODUCT_DEVICE}
'; }}
# shell variables
block={device.TARGET_BLOCK_DEVICE};
is_slot_device={is_ab};
ramdisk_compression=auto;
## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;
## AnyKernel install
{flash_procedure}
## end install
"""

FLASH_PROCEDURE_RAMDISK = """\
dump_boot;

write_boot;
"""

FLASH_PROCEDURE_NO_RAMDISK = """\
split_boot;

flash_boot;
flash_dtbo;
"""

INCLUDE_DATE_IN_ZIP_FILENAME = get_config("ak3.include_date_in_zip_filename", False)

def handle_remove_readonly(func, path, _):
	Path(path).chmod(S_IWRITE)
	func(path)

class AK3Manager:
	def __init__(self, device: Device):
		self.device = device

		self.device_out_path = out_path / self.device.PRODUCT_DEVICE
		self.path = self.device_out_path / "ANYKERNEL_OBJ"

		if self.path.is_dir():
			rmtree(self.path, ignore_errors=False, onerror=handle_remove_readonly)

		Repo.clone_from(ANYKERNEL3_REMOTE, self.path, single_branch=True, depth=1)

	def create_ak3_zip(self):
		artifacts = self.device_out_path / "KERNEL_OBJ" / "arch" / self.device.TARGET_ARCH / "boot"
		file_found = False
		for artifact in [artifacts / artifact for artifact in self.device.TARGET_BUILD_ARTIFACTS]:
			if not artifact.is_file():
				continue
			file_found = True
			copyfile(artifact, self.path / artifact.name)

		if file_found is False:
			LOGI("No artifact found, skipping AK3 zip creation")
			return

		with open(self.path / "anykernel.sh", 'w') as f:
			f.write(self.get_ak3_config())

		zip_filename = self.device_out_path / self.get_ak3_zip_filename()

		make_archive(zip_filename, 'zip', self.path)

		return f"{zip_filename}.zip"

	def get_ak3_config(self):
		is_ab = '1' if self.device.AB_OTA_UPDATER else '0'
		flash_procedure = (FLASH_PROCEDURE_RAMDISK
		                   if self.device.BOARD_BUILD_SYSTEM_ROOT_IMAGE
		                   else FLASH_PROCEDURE_NO_RAMDISK)

		text = AK3_CONFIG.format(device=self.device, kernel_name=KERNEL_NAME,
								 is_ab=is_ab, flash_procedure=flash_procedure)
		return text

	def get_ak3_zip_filename(self):
		filename = [KERNEL_NAME if KERNEL_NAME else "kernel"]
		filename.append(self.device.PRODUCT_DEVICE)
		if KERNEL_VERSION:
			filename.append(f"v{KERNEL_VERSION}")
		if INCLUDE_DATE_IN_ZIP_FILENAME:
			filename += [date.today().strftime('%Y%m%d')]

		return "-".join(filename)
