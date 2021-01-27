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

create_ak3_config() {
	if [ "$DEVICE_HAVE_NO_RAMDISK" = "true" ]; then
		local FLASH_PROCEDURE="split_boot;

flash_boot;
flash_dtbo;" >> "${ANYKERNEL_DIR}/anykernel.sh"
	else
		local FLASH_PROCEDURE="dump_boot;

write_boot;" >> "${ANYKERNEL_DIR}/anykernel.sh"
	fi

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
${FLASH_PROCEDURE}
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

generate_ak3_zip() {
	printf "Making flashable zip using anykernel3"

	cd "${ROOT_DIR}"

	# Always reclone AK3
	[ -d "${ANYKERNEL_DIR}" ] && rm -rf "${ANYKERNEL_DIR}"
	git clone https://github.com/osm0sis/AnyKernel3 "${ANYKERNEL_DIR}" -q

	# Include build artifacts in anykernel3 zip
	for i in $BUILD_ARTIFACTS; do
		cp "${OUT_DIR}/arch/${ARCH}/boot/${i}" "${ANYKERNEL_DIR}/${i}"
	done

	cd "${ANYKERNEL_DIR}"

	create_ak3_config
	create_ak3_zip_filename

	# Build a flashable zip using anykernel3
	zip -r9 "${AK3_ZIP_NAME}" * -x .git/ README.md "${AK3_ZIP_NAME}" > /dev/null

	echo ": done"

	# Return to initial pwd
	cd "${ROOT_DIR}"

	echo "Flashable zip: ${ANYKERNEL_DIR}/${AK3_ZIP_NAME}"
}
