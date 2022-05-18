from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.device import Device, devices
from build_kernel.utils.dumpvars import dumpvars
from build_kernel.utils.logging import LOGI
from build_kernel.utils.make import Make
from typing import Union

class Builder:
	"""Class representing a build instance."""
	def __init__(self, device: Device):
		"""Initialize the builder."""
		self.device = device

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

	def build(self, target: Union[str, list[str]] = None):
		"""Build the kernel and create an AnyKernel3 flashable zip."""
		LOGI("Building defconfig")
		self.make.run([self.device.TARGET_KERNEL_CONFIG] + self.device.TARGET_KERNEL_FRAGMENTS)

		LOGI("Building kernel")
		self.make.run(target)

		if target:
			return

		LOGI("Creating AnyKernel3 zip")
		zip_filename = self.ak3manager.create_ak3_zip()

		return zip_filename

	def clean(self):
		"""Clean output folder."""
		self.make.run("clean")
		self.make.run("mrproper")
