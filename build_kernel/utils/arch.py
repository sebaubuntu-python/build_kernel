from __future__ import annotations

class _Arch:
	_ALL: list[_Arch] = []

	def __init__(self, name: str, clang_triple_prefix: str):
		self.name = name
		self.clang_triple_prefix = clang_triple_prefix

		self._ALL.append(self)

	@classmethod
	def from_name(cls, name: str):
		for arch in cls._ALL:
			if name == arch.name:
				return arch

		raise ValueError(f"No arch with name: {name}")

class Arch(_Arch):
	ARM = _Arch("arm", "arm-linux-gnu-")
	ARM64 = _Arch("arm64", "aarch64-linux-gnu-")
	X86 = _Arch("x86", "x86_64-linux-gnu-")
	X86_64 = _Arch("x86_64", "x86_64-linux-gnu-")
