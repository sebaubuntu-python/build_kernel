from build_kernel import prebuilts_path, get_config
from build_kernel.utils.config import Config
from git import Repo
from logging import info
from multiprocessing import cpu_count
import os
from subprocess import Popen, PIPE, STDOUT
from typing import Optional

TOOLCHAINS_REMOTE = "https://github.com/SebaUbuntu/android-kernel-builder"
CLANG_VERSION = "r383902b"
GCC_VERSION = "4.9"

CLANG_PATH = prebuilts_path / "clang" / "linux-x86" / f"clang-{CLANG_VERSION}"
GCC_PATH = prebuilts_path / "gcc" / "linux-x86"
GCC_AARCH64_PATH = GCC_PATH / "aarch64" / f"aarch64-linux-android-{GCC_VERSION}"
GCC_ARM_PATH = GCC_PATH / "arm" / f"arm-linux-androideabi-{GCC_VERSION}"

class Make:
	def __init__(self, config: Config):
		self.config = config

		# Create environment variables
		self.env_vars = os.environ.copy()
		self.env_vars['PATH'] = f"{CLANG_PATH}/bin:{GCC_AARCH64_PATH}/bin:{GCC_ARM_PATH}/bin:{self.env_vars['PATH']}"

		# Create Make flags
		self.make_flags = [
			f"O={config.out_path}/KERNEL_OBJ",
			f"ARCH={config.arch}",
			f"SUBARCH={config.arch}",
			f"-j{cpu_count()}",
		]
		self.make_flags += [
			"CROSS_COMPILE=aarch64-linux-android-",
			"CROSS_COMPILE_ARM32=arm-linux-androideabi-"
		] if config.arch == "arm64" else [
			"CROSS_COMPILE=arm-linux-androideabi-"
		]
		self.make_flags += [
			f"CC=ccache {config.toolchain}"
		] if get_config("ENABLE_CCACHE") == "true" else [
			f"CC={config.toolchain}"
		]
		if config.toolchain == "clang":
			self.make_flags += [
				"CLANG_TRIPLE=aarch64-linux-gnu-"
			] if config.arch == "arm64" else [
				"CLANG_TRIPLE=arm-linux-gnu-"
			]

		localversion = ""
		kernel_name = get_config("COMMON_KERNEL_NAME")
		kernel_version = get_config("COMMON_KERNEL_VERSION")
		if kernel_name != "":
			localversion += f"-{kernel_name}"
		if kernel_version != "":
			localversion += f"-{kernel_version}"

		if localversion != "":
			self.make_flags += [f"LOCALVERSION={localversion}"]

		# Clone toolchains if needed
		for toolchain in ["clang", "gcc"]:
			toolchain_path = prebuilts_path / toolchain
			if toolchain_path.is_dir():
				continue

			info(f"Cloning toolchain: {toolchain}")
			Repo.clone_from(TOOLCHAINS_REMOTE, toolchain_path, branch=f"prebuilts-{toolchain}",
							single_branch=True, depth=1)
			info("Cloning finished")

	def run(self, target: Optional[str]=None):
		command = ["make"]
		command.extend(self.make_flags)
		if target is not None:
			command.append(target)

		process = Popen(command, env=self.env_vars, stdout=PIPE, stderr=STDOUT,
						cwd=self.config.kernel_path, encoding="UTF-8")
		while True:
			output = process.stdout.readline()
			if output == '' and process.poll() is not None:
				break
			if output:
				print(output.strip())
		rc = process.poll()
		if rc != 0:
			make_command = f'make {target}' if target is not None else 'make'
			raise RuntimeError(f"{make_command} failed, return code {rc}")

		return rc
