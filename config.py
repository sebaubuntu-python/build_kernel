config = {
	"ak3": {
		# type: bool
		# Include date in zip filename
		"include_date_in_zip_filename": True,
	},

	"build": {
		# type: bool
		# Enable ccache
		"enable_ccache": True,

		# type: str
		# Build user name, will set KBUILD_BUILD_USER
		"kbuild_build_user": "SebaUbuntu",

		# type: str
		# Build host name, will set KBUILD_BUILD_HOST
		"kbuild_build_host": "Seba-PC",

		# type: str
		# Common name of the kernel
		"kernel_name": "fratm",

		# type: str
		# Common version of the kernels
		"kernel_version": "1.0",
	},
}
