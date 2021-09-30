from build_kernel.utils.device import Device, register_device
# Note: if the kernel sources supports multiple devices,
# it's suggested to create a commonized config file and source it on the device-specific config
#from device.examples.common import ExamplesCommonDevice
#
#class ExamplesExampleDevice(ExamplesCommonDevice):

class ExamplesExampleDevice(Device):
	# Device codename
	PRODUCT_DEVICE = "example"
	# Device info
	TARGET_ARCH = "arm64"
	# Device defconfig
	TARGET_KERNEL_CONFIG = f"{PRODUCT_DEVICE}_defconfig"
	# Kernel sources location, in this case, must be in kernel/examples/example
	TARGET_KERNEL_SOURCE = "examples/example"
	# False: A-only (default), else True
	AB_OTA_UPDATER = False
	# False: It has a ramdisk in boot.img (default), else True
	BOARD_BUILD_SYSTEM_ROOT_IMAGE = True
	# Boot partition block path, default: /dev/block/bootdevice/by-name/boot
	DEVICE_BLOCK_PARTITION = "/dev/block/bootdevice/by-name/boot"
	# Building artifacts list (e.g. ["Image", "dtb.img"], or ["Image.gz-dtb"])
	BUILD_ARTIFACTS = ["Image.gz-dtb"]

# Put this line to add the device to the list of device configurations
#register_device(ExamplesExampleDevice)
