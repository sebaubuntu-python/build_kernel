#!/bin/sh
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

# Set defaults directories and variables
ROOT_DIR="$(pwd)"
ANYKERNEL_DIR="${ROOT_DIR}/anykernel3"
BUILD_DIR="${ROOT_DIR}/build"
TARGETS_DIR="${BUILD_DIR}/target"
CONFIGS_DIR="${ROOT_DIR}/configs"
KERNELS_DIR="${ROOT_DIR}/kernels"
OUT_DIR="${ROOT_DIR}/out"
PREBUILTS_DIR="${ROOT_DIR}/prebuilts"
DATE="$(date +"%m-%d-%y")"

build() {
	make "${MAKE_FLAGS[@]}" "$@"
}

create_localversion() {
	if [ "${COMMON_KERNEL_NAME}" != "" ]; then
		LOCALVERSION="${LOCALVERSION}-${COMMON_KERNEL_NAME}"
	fi
	if [ "${DEVICE_KERNEL_NAME}" != "" ]; then
		LOCALVERSION="${LOCALVERSION}-${DEVICE_KERNEL_NAME}"
	fi
	if [ "${COMMON_KERNEL_VERSION}" != "" ]; then
		LOCALVERSION="${LOCALVERSION}-${COMMON_KERNEL_VERSION}"
	fi
	if [ "${DEVICE_KERNEL_VERSION}" != "" ]; then
		LOCALVERSION="${LOCALVERSION}-${DEVICE_KERNEL_VERSION}"
	fi
}

setup_building_variables() {
	export PATH="${CLANG_PATH}/bin:${GCC_AARCH64_PATH}/bin:${GCC_ARM_PATH}/bin:${PATH}"

	TARGET_OUT_DIR="${OUT_DIR}/${DEVICE_CODENAME}"
	TARGET_KERNEL_OUT_DIR="${TARGET_OUT_DIR}/KERNEL_OBJ"

	MAKE_FLAGS=("O=${TARGET_KERNEL_OUT_DIR}" "ARCH=${ARCH}" "SUBARCH=${ARCH}" "-j$(nproc --all)")
	if [ "${ARCH}" = arm64 ]; then
		MAKE_FLAGS+=("CROSS_COMPILE=aarch64-linux-android-")
		MAKE_FLAGS+=("CROSS_COMPILE_ARM32=arm-linux-androideabi-")
	elif [ "${ARCH}" = arm ]; then
		MAKE_FLAGS=("CROSS_COMPILE=arm-linux-androideabi-")
	fi
	if [ "${ENABLE_CCACHE}" = "true" ]; then
		MAKE_FLAGS+=("CC=ccache ${TOOLCHAIN}")
	else
		MAKE_FLAGS+=("CC=${TOOLCHAIN}")
	fi
	if [ "${TOOLCHAIN}" = "clang" ]; then
		if [ "${ARCH}" = arm64 ]; then
			MAKE_FLAGS+=("CLANG_TRIPLE=aarch64-linux-gnu-")
		elif [ "${ARCH}" = arm ]; then
			MAKE_FLAGS+=("CLANG_TRIPLE=arm-linux-gnu-")
		fi
	fi
	if [ "${LOCALVERSION}" != "" ]; then
		MAKE_FLAGS+=("LOCALVERSION=$LOCALVERSION")
	fi
}

clone_toolchain() {
	for toolchain in "clang" "gcc"; do
		if [ ! -d "${PREBUILTS_DIR}/${toolchain}" ]; then
			echo "Cloning toolchain: ${toolchain}"
			git clone "${TOOLCHAINS_REMOTE}" "${PREBUILTS_DIR}/${toolchain}" -b "prebuilts-${toolchain}" --single-branch --depth=1
		fi
	done
}

print_summary() {
	echo -e "-----------------------------------------------------"
	echo    " Linux kernel version: ${LINUX_VERSION}              "
	echo    " Architecture: ${ARCH}                               "
	echo    " Last commit: ${KERNEL_LAST_COMMIT}                  "
	echo    " Sources directory: ${KERNEL_DIR}                    "
	echo    " Output directory: ${TARGET_OUT_DIR}                 "
	echo    " Build user: ${KBUILD_BUILD_USER}                    "
	echo    " Build machine: ${KBUILD_BUILD_HOST}                 "
	echo    " Build started on: $(date -d @${BUILD_START})        "
	if [ "${TOOLCHAIN}" = "clang" ]; then
	echo    " Toolchain: Clang ${CLANG_VERSION}                   "
	else
	echo    " Toolchain: GCC ${GCC_VERSION}                       "
	fi
	echo -e "-----------------------------------------------------"
}

execute_target() {
	echo "Running target: ${1}"
	_build_target_${1}
	local TARGET_SUCCESS=$?
	if [ "${TARGET_SUCCESS}" != 0 ]; then
		echo "${red}${1}: FAILED, error ${TARGET_SUCCESS}${reset}"
		exit
	fi
	return "${TARGET_SUCCESS}"
}
