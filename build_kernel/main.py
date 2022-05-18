from argparse import ArgumentParser
from build_kernel.builder import Builder
from build_kernel.utils.device import devices
from build_kernel.utils.logging import LOGE, LOGI, setup_logging

def main():
	setup_logging()

	parser = ArgumentParser(prog='python3 -m kernel_build')

	# Positional arguments
	parser.add_argument("device", type=str, help="device codename")

	# Build tasks
	parser.add_argument("-c", "--clean", action='store_true', help="cleanup out dir")

	# Build options
	parser.add_argument("-v", "--verbose", action='store_true', help="verbose logging")

	args, build_target = parser.parse_known_args()

	builder = Builder.from_codename(args.device)
	if not builder:
		LOGE(f"Device {args.device} not found")
		LOGI("Available devices:\n" + "\n".join(devices.keys()))
		return

	builder.dumpvars()

	if args.clean:
		builder.clean()
		return

	zip_filename = builder.build(build_target)

	LOGI(f"Build completed successfully: {zip_filename}")
