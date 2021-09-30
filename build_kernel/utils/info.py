from build_kernel import get_config
from build_kernel.utils.config import Config

def print_summary(config: Config):
	print("\n".join([
		"============================================",
		f"KERNEL_VERSION={config.kernel_version}",
		f"TARGET_ARCH={config.arch}",
		f"TARGET_KERNEL_SOURCES={config.kernel_path}",
		f"OUT_DIR={config.out_path}",
		f"BUILD_USER={get_config('KBUILD_BUILD_USER')}",
		f"BUILD_HOST={get_config('KBUILD_BUILD_HOST')}",
		f"CCACHE={get_config('ENABLE_CCACHE')}",
		"============================================",
	]))
