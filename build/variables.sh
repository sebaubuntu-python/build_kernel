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

# Toolchain repos
TOOLCHAINS_REMOTE="https://github.com/SebaUbuntu/android-kernel-builder"

# GCC path
GCC_VERSION=4.9
GCC_PATH="${PREBUILTS_DIR}/gcc/linux-x86"
GCC_AARCH64_PATH="${GCC_PATH}/aarch64/aarch64-linux-android-${GCC_VERSION}"
GCC_ARM_PATH="${GCC_PATH}/arm/arm-linux-androideabi-${GCC_VERSION}"

# Clang path
CLANG_VERSION=r383902b
CLANG_PATH="${PREBUILTS_DIR}/clang/linux-x86/clang-${CLANG_VERSION}"

# Color definition
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`
