from build_kernel import toolchains_path
from build_kernel.utils.arch import Arch
from build_kernel.utils.logging import LOGI
from git.repo import Repo
from pathlib import Path
from typing import List, Optional

class _Toolchain:
	def __init__(self, name: str, path: Path, url: Optional[str], cc: str):
		self.name = name
		self.path = path
		self.url = url
		self.cc = cc

	def prepare(self, arch: Arch) -> None:
		if not self.url:
			return

		if not self.path.exists():
			LOGI(f"Toolchain {self.name} not found at {self.path}, cloning")
			Repo.clone_from(self.url, self.path, branch=self.name,
			                single_branch=True, depth=1)
			LOGI(f"Toolchain {self.name} cloned")

	def get_path_dirs(self, arch: Arch) -> List[Path]:
		path_dirs = []

		return path_dirs

	def get_make_flags(self, arch: Arch) -> List[str]:
		make_flags = []

		make_flags.append('CPATH="/usr/include:/usr/include/x86_64-linux-gnu"')
		make_flags.append('HOSTLDFLAGS="-L/usr/lib/x86_64-linux-gnu -L/usr/lib64 -fuse-ld=lld"')

		return make_flags

class _GccToolchain(_Toolchain):
	BASE_PATH = toolchains_path / "gcc"
	BASE_REMOTE = "https://github.com/SebaUbuntu/toolchains_gcc"

	def __init__(self, version: str, prefix: str, url: Optional[str] = BASE_REMOTE):
		super().__init__(version, self.BASE_PATH / version, url, "gcc" if not prefix else f"{prefix}gcc")

		self.prefix = prefix

	def get_path_dirs(self, arch: Arch) -> List[Path]:
		path_dirs = super().get_path_dirs(arch)

		path_dirs.append(self.path / "bin")

		return path_dirs

	def get_make_flags(self, arch: Arch) -> List[str]:
		make_flags = super().get_make_flags(arch)

		make_flags.append(f"CROSS_COMPILE={self.prefix}")

		if arch == Arch.ARM:
			# Avoid "Unknown symbol _GLOBAL_OFFSET_TABLE_" errors
			make_flags.append('CFLAGS_MODULE="-fno-pic"')

		if arch == Arch.ARM64:
			# Avoid "unsupported RELA relocation: 311" errors (R_AARCH64_ADR_GOT_PAGE)
			make_flags.append('CFLAGS_MODULE="-fno-pic"')

		return make_flags

class GccToolchain(_GccToolchain):
	VERSIONS = {
		"arm-linux-androideabi-4.9": _GccToolchain("arm-linux-androideabi-4.9", "arm-linux-androideabi-"),
		"aarch64-linux-android-4.9": _GccToolchain("aarch64-linux-android-4.9", "aarch64-linux-android-"),
		"x86_64-linux-android-4.9": _GccToolchain("x86_64-linux-android-4.9", "x86_64-linux-android-"),
	}
	DEFAULT_ARM = VERSIONS["arm-linux-androideabi-4.9"]
	DEFAULT_ARM64 = VERSIONS["aarch64-linux-android-4.9"]
	DEFAULT_X86 = VERSIONS["x86_64-linux-android-4.9"]
	DEFAULT_X86_64 = VERSIONS["x86_64-linux-android-4.9"]

	@classmethod
	def from_version(cls, version: str) -> _GccToolchain:
		if version in cls.VERSIONS:
			return cls.VERSIONS[version]
		else:
			raise ValueError(f"No toolchain for version: {version}")

	@classmethod
	def get_default(cls, arch: Arch) -> _GccToolchain:
		if arch is Arch.ARM:
			return cls.DEFAULT_ARM
		elif arch is Arch.ARM64:
			return cls.DEFAULT_ARM64
		elif arch is Arch.X86:
			return cls.DEFAULT_X86
		elif arch is Arch.X86_64:
			return cls.DEFAULT_X86_64
		else:
			raise ValueError(f"No default toolchain for arch: {arch}")

class _ClangToolchain(_Toolchain):
	BASE_PATH = toolchains_path / "clang"
	BASE_REMOTE = "https://github.com/SebaUbuntu/toolchains_clang"

	def __init__(self, version: str):
		super().__init__(version, self.BASE_PATH / version, self.BASE_REMOTE, "clang")

	def prepare(self, arch: Arch) -> None:
		super().prepare(arch)

		GccToolchain.get_default(arch).prepare(arch)

		# Needed for CONFIG_COMPAT_VDSO
		if arch is Arch.ARM64:
			GccToolchain.get_default(Arch.ARM).prepare(arch)

	def get_path_dirs(self, arch: Arch) -> List[Path]:
		path_dirs = super().get_path_dirs(arch)

		default_gcc = GccToolchain.get_default(arch)

		path_dirs.extend(default_gcc.get_path_dirs(arch))

		path_dirs.append(self.path / "bin")

		# Needed for CONFIG_COMPAT_VDSO
		if arch is Arch.ARM64:
			path_dirs.extend(GccToolchain.get_default(Arch.ARM).get_path_dirs(arch))

		return path_dirs

	def get_make_flags(self, arch: Arch) -> List[str]:
		default_gcc = GccToolchain.get_default(arch)

		make_flags = default_gcc.get_make_flags(arch)

		make_flags.append(f"CLANG_TRIPLE={arch.clang_triple_prefix}")

		# Needed for CONFIG_COMPAT_VDSO
		if arch is Arch.ARM64:
			make_flags.append(f"CROSS_COMPILE_ARM32={GccToolchain.get_default(Arch.ARM).prefix}")

		# Set the full path to the clang command and LLVM binutils
		make_flags.append(f"HOSTCC={self.path / 'bin' / 'clang'}")
		make_flags.append(f"HOSTCXX={self.path / 'bin' / 'clang++'}")

		return make_flags

class ClangToolchain(_ClangToolchain):
	VERSIONS = {
		"r416183b1": _ClangToolchain("r416183b1"),
	}
	DEFAULT = VERSIONS["r416183b1"]

	@classmethod
	def from_version(cls, version: str) -> _ClangToolchain:
		if version in cls.VERSIONS:
			return cls.VERSIONS[version]
		else:
			raise ValueError(f"No toolchain for version: {version}")
