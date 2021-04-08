from build_kernel import get_config
from build_kernel.utils.config import Config
from datetime import date
from git import Repo
from logging import info
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
device.name1={config.codename}
'; }}
# shell variables
block={config.block_device};
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


def handle_remove_readonly(func, path, _):
	Path(path).chmod(S_IWRITE)
	func(path)

class AK3Manager:
	def __init__(self, config: Config):
		self.config = config
		self.path = config.out_path / "ANYKERNEL_OBJ"
		self.kernel_name = get_config("COMMON_KERNEL_NAME")
		self.kernel_version = get_config("COMMON_KERNEL_VERSION")

		if self.path.is_dir():
			rmtree(self.path, ignore_errors=False, onerror=handle_remove_readonly)

		Repo.clone_from(ANYKERNEL3_REMOTE, self.path, single_branch=True, depth=1)

	def create_ak3_zip(self):
		artifacts = self.config.out_path / "KERNEL_OBJ" / "arch" / self.config.arch / "boot"
		file_found = False
		for artifact in self.config.build_artifacts:
			artifact_path = artifacts / artifact
			if not artifact_path.is_file():
				continue
			file_found = True
			copyfile(artifact_path, self.path / artifact)

		if file_found is False:
			info("No artifact found, skipping AK3 zip creation")
			return

		with open(self.path / "anykernel.sh", 'w') as f:
			f.write(self.get_ak3_config())

		make_archive(self.config.out_path / self.get_ak3_zip_filename(), 'zip', self.path)

	def get_ak3_config(self):
		is_ab = '1' if self.config.is_ab else '0'
		flash_procedure = FLASH_PROCEDURE_RAMDISK if self.config.has_ramdisk else FLASH_PROCEDURE_NO_RAMDISK

		text = AK3_CONFIG.format(config=self.config, kernel_name=self.kernel_name,
								 is_ab=is_ab, flash_procedure=flash_procedure)
		return text

	def get_ak3_zip_filename(self):
		filename = [self.kernel_name if self.kernel_name != "" else "kernel"]
		filename += [self.config.codename, self.kernel_version]
		if get_config("INCLUDE_DATE_IN_ZIP_FILENAME") == "true":
			filename += [date.today().strftime('%Y%m%d')]

		return "-".join(filename)
