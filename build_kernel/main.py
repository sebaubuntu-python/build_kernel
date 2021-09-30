from build_kernel.utils.ak3 import AK3Manager
from build_kernel.utils.cc import Make
from build_kernel.utils.config import load_config_module
from build_kernel.utils.info import print_summary
from build_kernel.utils.logging import LOGI
from pathlib import Path

def main(config_path: Path, clean=False):
	config = load_config_module(config_path)
	make = Make(config)

	print_summary(config)

	(config.out_path / "KERNEL_OBJ").mkdir(exist_ok=True, parents=True)

	if clean is True:
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
