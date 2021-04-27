from build_kernel import device_path, root_path, out_path
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

class Config:
	codename: str
	kernel_path: Path
	kernel_version: str
	arch: str
	defconfig: str
	is_ab: bool
	has_ramdisk: bool
	block_device: str
	build_artifacts: list[str]
	toolchain: str

	def __init__(self, config):
		self.codename = config.CODENAME
		self.kernel_path = root_path / config.KERNEL_PATH
		self.kernel_version = config.KERNEL_VERSION
		self.arch = config.ARCH
		self.defconfig = config.DEFCONFIG
		self.is_ab = config.IS_AB
		self.has_ramdisk = config.HAS_RAMDISK
		self.block_device = config.BLOCK_DEVICE
		self.build_artifacts = config.BUILD_ARTIFACTS
		self.toolchain = config.TOOLCHAIN
		self.out_path = out_path / self.codename
		try:
			self.additional_make_flags = config.ADDITIONAL_MAKE_FLAGS
		except AttributeError:
			self.additional_make_flags = []

def load_config_module(config_path: Path):
	spec = spec_from_file_location("config", device_path / f"{config_path}.py")
	config_module = module_from_spec(spec)
	spec.loader.exec_module(config_module)
	return Config(config_module)
