from build_kernel.utils.device import register_devices
from dotenv import load_dotenv
import os
from pathlib import Path

__version__ = "1.0.0"

current_path = Path(os.getcwd())

module_path = Path(__file__).parent
root_path = module_path.parent
device_path = root_path / "device"
kernel_path = root_path / "kernel"
out_path = root_path / "out"
prebuilts_path = root_path / "prebuilts"

get_config = os.environ.get

load_dotenv(root_path / "config.env")
register_devices(device_path)
