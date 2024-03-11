from build_kernel import out_path
from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.device import Device, devices
from build_kernel.utils.dumpvars import dumpvars
from build_kernel.utils.logging import LOGI
from build_kernel.utils.make import Make
from build_kernel.utils.mkdtboimg import Dtbo, parse_create_args, parse_dt_entries
from typing import List, Optional, Union

class Builder:
	"""Class representing a build instance."""
	def __init__(self, device: Device):
		"""Initialize the builder."""
		self.device = device

		self.out_path = out_path / self.device.PRODUCT_DEVICE

		self.dtb_out = self.out_path / "dtb.img"
		self.dtbo_out = self.out_path / "dtbo.img"

		self.kernel_obj_path = self.out_path / "KERNEL_OBJ"
		self.kernel_obj_boot_path = self.kernel_obj_path / "arch" / self.device.TARGET_ARCH / "boot"
		self.dtbs_path = self.kernel_obj_boot_path / "dts"

		self.make = Make(self.device)
		self.ak3manager = AK3Manager(self.device)

	@classmethod
	def from_codename(cls, codename: str):
		"""Get a Builder object for the given device codename."""
		if not codename in devices:
			return None

		return cls(devices[codename])

	def dumpvars(self):
		"""Dump the kernel variables to stdout."""
		return dumpvars(self.device)

	def build(self, target: Union[str, Optional[List[str]]] = None):
		"""Build the kernel and create an AnyKernel3 flashable zip."""
		LOGI("Building defconfig")
		self.make.run([self.device.TARGET_KERNEL_CONFIG] + self.device.TARGET_KERNEL_FRAGMENTS)

		LOGI("Building kernel")
		self.make.run(target)

		if target:
			return

		artifacts = [self.kernel_obj_boot_path / self.device.BOARD_KERNEL_IMAGE_NAME]

		if self.device.BOARD_INCLUDE_DTB_IN_BOOTIMG:
			dtb_files = [file for file in self.dtbs_path.rglob("*.dtb")]
			assert dtb_files, "No dtb files found"
			with self.dtb_out.open("wb") as f:
				for dtb_file in dtb_files:
					f.write(dtb_file.read_bytes())

			artifacts.append(self.dtb_out)

		if self.device.BOARD_KERNEL_SEPARATED_DTBO:
			dtbo_files = [str(file) for file in self.dtbs_path.rglob("*.dtbo")]
			assert dtbo_files, "No dtbo files found"
			global_args, _ = parse_create_args([])
			dt_entries = parse_dt_entries(global_args, dtbo_files)
			with self.dtbo_out.open("wb") as f:
				dtbo = Dtbo(f, page_size=self.device.BOARD_KERNEL_PAGESIZE)
				dt_entry_buf = dtbo.add_dt_entries(dt_entries)
				dtbo.commit(dt_entry_buf)

			artifacts.append(self.dtbo_out)

		if not artifacts:
			LOGI("No artifact found, skipping AK3 zip creation")
			return

		LOGI("Creating AnyKernel3 zip")
		zip_filename = self.ak3manager.create_ak3_zip(artifacts)

		return zip_filename

	def clean(self):
		"""Clean output folder."""
		self.make.run("clean")
		self.make.run("mrproper")
