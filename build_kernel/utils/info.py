from build_kernel import get_config
from build_kernel.utils.config import Config

TEXT = """\
============================================
Linux kernel version={config.kernel_version}
Architecture={config.arch}
Sources directory={config.kernel_path}
Output directory={out_path}
Build user={build_user}
Build machine={build_host}
Toolchain={config.toolchain}
ccache enabled={ccache}
============================================
"""

def print_summary(config: Config):
	text = TEXT.format(config=config, out_path=config.out_path,
					   build_user=get_config("KBUILD_BUILD_USER"),
					   build_host=get_config("KBUILD_BUILD_HOST"),
					   ccache=get_config("ENABLE_CCACHE"))
	print(text)
