#!/bin/bash
#
# Copyright (C) 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Make pipelines return last non-zero exit code
set -o pipefail

source "build/core.sh"
source "build/ak3.sh"
source "build/variables.sh"
source "${ROOT_DIR}/settings.conf"

while [ "${#}" -gt 0 ]; do
	case "${1}" in
		-c | --clean )
			CLEAN="true"
			;;
		--kernel-headers )
			KERNEL_HEADERS="true"
			;;
		* )
			PROJECT="${1}"
			;;
	esac
	shift
done

# Source config files
if [ ! -f "${CONFIGS_DIR}/${PROJECT}" ]; then
	echo "Error: project configuration file not found"
	exit
fi
source "${CONFIGS_DIR}/${PROJECT}"

KERNEL_DIR="${KERNELS_DIR}/${KERNEL_DIR_NAME}"

# Set kernel source workspace
cd "${KERNEL_DIR}"

KERNEL_LAST_COMMIT=$(git log -1 --format="%h")
if [ "${KERNEL_LAST_COMMIT}" = "" ]; then
	KERNEL_LAST_COMMIT="Unknown"
fi

create_localversion
setup_building_variables
clone_toolchain

[ ! -d "${TARGET_OUT_DIR}" ] && mkdir -p "${TARGET_OUT_DIR}"

BUILD_START="$(date +'%s')"

print_summary

# Clean
if [ "${CLEAN}" = "true" ]; then
	printf "Running command: make clean"
	build clean &> "${TARGET_OUT_DIR}/clean_log.txt"
	CLEAN_SUCCESS=$?
	if [ "${CLEAN_SUCCESS}" != 0 ]; then
		echo "${red}Error: make clean failed${reset}"
		exit
	else
		echo ": done"
	fi

	printf "Running command: make mrproper"
	build mrproper &> "${TARGET_OUT_DIR}/mrproper_log.txt"
	MRPROPER_SUCCESS=$?
	if [ "${MRPROPER_SUCCESS}" != 0 ]; then
		echo "${red}Error: make mrproper failed${reset}"
		exit
	else
		echo ": done"
	fi
fi

# Make defconfig
printf "Running command: make ${DEFCONFIG}"
build "${DEFCONFIG}" &> ${TARGET_OUT_DIR}/defconfig_log.txt

DEFCONFIG_SUCCESS=$?
if [ "${DEFCONFIG_SUCCESS}" != 0 ]; then
	echo "${red}Error: make ${DEFCONFIG} failed, specified a defconfig not present?${reset}"
	exit
else
	echo ": done"
fi

if [ "${KERNEL_HEADERS}" != "true" ]; then
	# Build kernel
	echo "Running command: make"
	build | tee "${TARGET_OUT_DIR}/build_log.txt" | while read i; do printf "%-${COLUMNS}s\r" "$i"; done
else
	# Build kernel headers
	echo "Running command: make headers_install"
	build headers_install | tee "${TARGET_OUT_DIR}/build_log.txt" | while read i; do printf "%-${COLUMNS}s\r" "$i"; done
fi

BUILD_SUCCESS=$?
BUILD_END=$(date +"%s")
DIFF=$(($BUILD_END - $BUILD_START))
printf "%-${COLUMNS}s\r"
if [ "${BUILD_SUCCESS}" != 0 ]; then
	echo "${red}Error: Build failed in $(($DIFF / 60)) minute(s) and $(($DIFF % 60)) seconds${reset}"
	exit
fi

echo ""
echo -e "${green}Build completed in $(($DIFF / 60)) minute(s) and $(($DIFF % 60)) seconds${reset}"
echo ""

[ "${KERNEL_HEADERS}" = "true" ] && exit

generate_ak3_zip

echo "${green}All done${reset}"
