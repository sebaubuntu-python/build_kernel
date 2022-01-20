"""Android kernel builder module."""

from build_kernel.utils.device import register_devices
import os
from pathlib import Path

# I'm sorry
try:
	from config import config
except ModuleNotFoundError:
	config = {}

__version__ = "1.0.0"

module_path = Path(__file__).parent
current_path = Path(os.getcwd())

root_path = module_path.parent
device_path = root_path / "device"
kernel_path = root_path / "kernel"
out_path = root_path / "out"
prebuilts_path = root_path / "prebuilts"

register_devices(device_path)
