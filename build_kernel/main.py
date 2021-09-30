from argparse import ArgumentParser
from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.cc import Make
from build_kernel.utils.config import load_config_module
from build_kernel.utils.info import print_summary
from build_kernel.utils.logging import LOGI
from pathlib import Path

def main():
	parser = ArgumentParser(prog='python3 -m kernel_build')

	parser.add_argument("config", type=Path,
						help="device configuration file")
	parser.add_argument("-c", "--clean", action='store_true',
						help="clean before building")
	parser.add_argument("-v", "--verbose", action='store_true',
						help="verbose logging")

	args = parser.parse_args()

	config = load_config_module(args.config)
	make = Make(config)

	print_summary(config)

	(config.out_path / "KERNEL_OBJ").mkdir(exist_ok=True, parents=True)

	if args.clean is True:
		LOGI("Cleaning before building")
		make.run("clean")
		make.run("mrproper")

	LOGI("Building defconfig")
	make.run(config.defconfig)

	LOGI("Building kernel")
	make.run()

	LOGI("Creating AnyKernel3 zip")
	ak3manager = AK3Manager(config)
	zip_filename = ak3manager.create_ak3_zip()

	LOGI(f"Build completed successfully: {zip_filename}")
