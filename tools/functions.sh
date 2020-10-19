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

	MAKE_FLAGS="O=$OUT_DIR ARCH=$ARCH SUBARCH=$ARCH -j$(nproc --all)"
	if [ $ARCH = arm64 ]; then
		MAKE_FLAGS="${MAKE_FLAGS} CROSS_COMPILE=aarch64-linux-android- CROSS_COMPILE_ARM32=arm-linux-androideabi-"
	elif [ $ARCH = arm ]; then
		MAKE_FLAGS="${MAKE_FLAGS} CROSS_COMPILE=arm-linux-androideabi-"
	fi
	if [ "${TOOLCHAIN}" = "clang" ]; then
		MAKE_FLAGS="${MAKE_FLAGS} CC=clang"
		if [ "${ARCH}" = arm64 ]; then
			MAKE_FLAGS="${MAKE_FLAGS} CLANG_TRIPLE=aarch64-linux-gnu-"
		elif [ "${ARCH}" = arm ]; then
			MAKE_FLAGS="${MAKE_FLAGS} CLANG_TRIPLE=arm-linux-gnu-"
		fi
	fi
	if [ "${LOCALVERSION}" != "" ]; then
		MAKE_FLAGS="${MAKE_FLAGS} LOCALVERSION=$LOCALVERSION"
	fi
}

print_summary() {
	echo -e "-----------------------------------------------------"
	echo    " Linux kernel version: ${LINUX_VERSION}              "
	echo    " Architecture: ${ARCH}                               "
	echo    " Last commit: ${KERNEL_LAST_COMMIT}                  "
	echo    " Sources directory: ${KERNEL_DIR}                    "
	echo    " Output directory: ${OUT_DIR}                        "
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

create_ak3_config() {
	rm "${ANYKERNEL_DIR}/anykernel.sh"
	echo "# AnyKernel3 Ramdisk Mod Script
# osm0sis @ xda-developers

## AnyKernel setup
# begin properties
properties() { '
kernel.string=${KERNEL_NAME}
do.devicecheck=1
do.modules=0
do.systemless=1
do.cleanup=1
do.cleanuponabort=0
device.name1=${DEVICE_CODENAME}
'; }

# shell variables
block=${DEVICE_BLOCK_PARTITION};
is_slot_device=${DEVICE_IS_AB};
ramdisk_compression=auto;

## AnyKernel methods (DO NOT CHANGE)
# import patching functions/variables - see for reference
. tools/ak3-core.sh;

## AnyKernel install
dump_boot;

write_boot;
## end install
" >> "${ANYKERNEL_DIR}/anykernel.sh"
}

create_ak3_zip_filename() {
	if [ "${COMMON_KERNEL_NAME}" != "" ] && [ "${DEVICE_KERNEL_NAME}" != "" ]; then
		AK3_ZIP_NAME="${COMMON_KERNEL_NAME}-${DEVICE_KERNEL_NAME}"
	elif [ "${COMMON_KERNEL_NAME}" != "" ]; then
		AK3_ZIP_NAME="${COMMON_KERNEL_NAME}"
	elif [ "${DEVICE_KERNEL_NAME}" != "" ]; then
		AK3_ZIP_NAME="${DEVICE_KERNEL_NAME}"
	else
		AK3_ZIP_NAME="kernel"
	fi
	AK3_ZIP_NAME="${AK3_ZIP_NAME}-${DEVICE_CODENAME}"
	if [ "${COMMON_KERNEL_VERSION}" != "" ]; then
		AK3_ZIP_NAME="${AK3_ZIP_NAME}-${COMMON_KERNEL_VERSION}"
	fi
	if [ "${DEVICE_KERNEL_VERSION}" != "" ]; then
		AK3_ZIP_NAME="${AK3_ZIP_NAME}-${DEVICE_KERNEL_VERSION}"
	fi
	if [ "${INCLUDE_DATE_IN_ZIP_FILENAME}" = "true" ]; then
		AK3_ZIP_NAME="${AK3_ZIP_NAME}-${DATE}"
	fi
	AK3_ZIP_NAME="${AK3_ZIP_NAME}.zip"
}
