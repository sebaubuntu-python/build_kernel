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
source "build/variables.sh"
source "${ROOT_DIR}/settings.conf"

# Source targets
for target in $(ls "${TARGETS_DIR}"); do
	source "${TARGETS_DIR}/${target}"
done

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

[ ! -d "${TARGET_KERNEL_OUT_DIR}" ] && mkdir -p "${TARGET_KERNEL_OUT_DIR}"

BUILD_START="$(date +'%s')"

print_summary

# Clean
if [ "${CLEAN}" = "true" ]; then
	execute_target clean
fi

if [ "${KERNEL_HEADERS}" != "true" ]; then
	execute_target kernel
else
	execute_target kernel_headers
fi

BUILD_END=$(date +"%s")
DIFF=$(($BUILD_END - $BUILD_START))

echo ""
echo -e "${green}Build completed in $(($DIFF / 60)) minute(s) and $(($DIFF % 60)) seconds${reset}"
echo ""
