"""Android kernel builder module."""

from build_kernel.utils.device import register_devices
from pathlib import Path

# I'm sorry
try:
	from config import config
except ModuleNotFoundError:
	config = {}

__version__ = "1.1.0"

module_path = Path(__file__).parent
current_path = Path.cwd()

device_path = current_path / "device"
kernel_path = current_path / "kernel"
out_path = current_path / "out"
toolchains_path = current_path / "toolchains"

register_devices(device_path)
