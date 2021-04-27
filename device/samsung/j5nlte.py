# Source common kernel config
from device.samsung.msm8916 import *

# Device info
CODENAME = "j5nlte"
ADDITIONAL_MAKE_FLAGS = ["VARIANT_DEFCONFIG=msm8916_sec_j5nlte_eur_defconfig"]

IS_AB = False
HAS_RAMDISK = True
