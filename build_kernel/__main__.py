#!/usr/bin/python3

from argparse import ArgumentParser
from build_kernel.main import main
from pathlib import Path

if __name__ == '__main__':
	parser = ArgumentParser(prog='python3 -m kernel_build')

	parser.add_argument("config", type=Path,
						help="device configuration file")

	parser.add_argument("-c", "--clean", action='store_true',
						help="clean before building")
	parser.add_argument("-v", "--verbose", action='store_true',
						help="verbose logging")

	args = parser.parse_args()

	main(args.config, clean=args.clean)
