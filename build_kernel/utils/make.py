from build_kernel import current_path, out_path
from build_kernel.utils.arch import Arch
from build_kernel.utils.config import get_config
from build_kernel.utils.device import Device
from build_kernel.utils.toolchain import ClangToolchain, GccToolchain
from multiprocessing import cpu_count
import os
from pathlib import Path
import platform
from subprocess import Popen, PIPE, STDOUT
from typing import Union

ENABLE_CCACHE = get_config("build.enable_ccache", False)
KERNEL_NAME = get_config("build.kernel_name")
KERNEL_VERSION = get_config("build.kernel_version")
KBUILD_BUILD_USER = get_config("build.kbuild_build_user")
KBUILD_BUILD_HOST = get_config("build.kbuild_build_host")

SUPPORTED_ENVIRONMENTS: list[tuple[str, str]] = [
	("64bit", "ELF"),
]
"""List of supported arch/system combos."""

class Make:
	def __init__(self, device: Device):
		self.device = device

		host_architecture = platform.architecture()
		if host_architecture not in SUPPORTED_ENVIRONMENTS:
			raise RuntimeError(f"Unsupported environment: {host_architecture}")

		self.kernel_source = current_path / self.device.TARGET_KERNEL_SOURCE
		self.out_path = out_path / device.PRODUCT_DEVICE / "KERNEL_OBJ"
		self.out_path.mkdir(exist_ok=True, parents=True)

		self.arch = Arch.from_name(self.device.TARGET_ARCH)

		if device.TARGET_KERNEL_CLANG_COMPILE:
			self.toolchain = (ClangToolchain.from_version(device.TARGET_KERNEL_CLANG_VERSION)
			                  if device.TARGET_KERNEL_CLANG_VERSION
			                  else ClangToolchain.DEFAULT)
		else:
			self.toolchain = (GccToolchain.from_version(device.TARGET_KERNEL_GCC_VERSION)
			                  if device.TARGET_KERNEL_GCC_VERSION
			                  else GccToolchain.get_default(self.arch))

		self.toolchain.prepare(self.arch)

		self.path_dirs: list[Path] = []
		self.path_dirs.extend(self.toolchain.get_path_dirs(self.arch))

		# Create environment variables
		self.env_vars = os.environ.copy()
		self.env_vars['PATH'] = f"{':'.join([str(path) for path in self.path_dirs])}:{self.env_vars['PATH']}"

		# Create Make flags
		self.make_flags = [
			f"O={self.out_path}",
			f"ARCH={self.arch.name}",
			f"SUBARCH={self.arch.name}",
			f"-j{cpu_count()}",
		]

		self.make_flags.extend(self.toolchain.get_make_flags(self.arch))

		if ENABLE_CCACHE:
			self.make_flags.append(f"CC=ccache {self.toolchain.cc}")
		else:
			self.make_flags.append(f"CC={self.toolchain.cc}")

		localversion = ""
		if KERNEL_NAME:
			localversion += f"-{KERNEL_NAME}"
		if KERNEL_VERSION:
			localversion += f"-{KERNEL_VERSION}"

		if localversion:
			self.make_flags.append(f"LOCALVERSION={localversion}")

		if KBUILD_BUILD_USER:
			self.make_flags.append(f"KBUILD_BUILD_USER={KBUILD_BUILD_USER}")
		if KBUILD_BUILD_HOST:
			self.make_flags.append(f"KBUILD_BUILD_HOST={KBUILD_BUILD_HOST}")

		self.make_flags += device.TARGET_ADDITIONAL_MAKE_FLAGS

	def run(self, target: Union[str, list] = None):
		command = ["make"]
		command.extend(self.make_flags)
		if target is not None:
			if isinstance(target, str):
				command.append(target)
			else:
				command.extend(target)

		process = Popen(command, env=self.env_vars, stdout=PIPE, stderr=STDOUT,
						cwd=self.kernel_source, encoding="UTF-8")
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		rc = process.poll()
		if rc != 0:
			make_command = "make"
			if target is not None:
				make_command += f" {target}"

			raise RuntimeError(f"{make_command} failed, return code {rc}")

		return rc
