from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.cc import Make
from build_kernel.utils.config import load_config_module
from build_kernel.utils.info import print_summary
from logging import info
from pathlib import Path

def main(config_path: Path, clean=False):
	config = load_config_module(config_path)
	make = Make(config)

	print_summary(config)

	(config.out_path / "KERNEL_OBJ").mkdir(exist_ok=True, parents=True)

	if clean is True:
		info("Cleaning before building")
		make.run("clean")
		make.run("mrproper")

	info("Building defconfig")
	make.run(config.defconfig)

	info("Building kernel")
	make.run()

	info("Creating AnyKernel3 zip")
	ak3manager = AK3Manager(config)
	zip_filename = ak3manager.create_ak3_zip()

	info(f"Build completed successfully: {zip_filename}")
