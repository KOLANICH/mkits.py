import typing
from pathlib import Path

from fdt import Node, PropStrings, PropWords, FDT

__all__ = ("genITS", "__copyright__")

__copyright__ = """
Licensed under the terms of the GNU GPL License version 3 or later.

Author: Peter Tyser <ptyser@xes-inc.com>
Rewritten into python by: KOLANICH <KOLANICH@users.noreply.github.com>
"""

__doc__ = """
U-Boot firmware supports the booting of images in the Flattened Image
Tree (FIT) format.  The FIT format uses a device tree structure to
describe a kernel image, device tree blob, ramdisk, etc.  This script
creates an Image Tree Source (.its file) which can be passed to the
'mkimage' utility to generate an Image Tree Blob (.itb file).  The .itb
file can then be booted by U-Boot (or other bootloaders which support
FIT images).  See doc/uImage.FIT/howto.txt in U-Boot source code for
additional information on FIT images.
"""


# DEFAULT_INCBIN = Path("./incbin/").absolute()
DEFAULT_INCBIN = Path("./").absolute()

DEFAULT_CHECKSUM_ALGOS = ("crc32", "sha1")


def genITS(arch: str, osName: str, kernel_image: Path, kernel_ver: str, load_addr: int, entry_addr: int, config: Path, fdtnum: int, compression: str, checksumAlgos: typing.Iterable[str] = DEFAULT_CHECKSUM_ALGOS, human_name: typing.Optional[str] = None, device_tree_blob: typing.Optional[Path] = None, incbin: Path = DEFAULT_INCBIN, component: str="kernel") -> Node:
	arch_upper = arch.upper()
	checksum_algos = [Node("hash@" + str(i + 1), PropStrings("algo", el)) for i, el in enumerate(checksumAlgos)]

	append_to_images = []

	config_rel_str = str(config.relative_to(incbin).stem)

	componentName = component + "@1"

	images = Node(
		"images",
		Node(
			componentName,
			PropStrings("description", arch_upper + " OpenWrt Linux-" + str(kernel_ver)),
			# data = /incbin/("'''+ str(kernel_image.relative_to(incbin)) + '''");
			PropStrings("type", component),
			PropStrings("arch", arch),
			PropStrings("os", osName),
			PropStrings("compression", compression),
			PropWords("load", load_addr),
			PropWords("entry", entry_addr),
			*checksum_algos,
		),
	)

	target_comp = Node(
		config_rel_str,
		PropStrings("description", "OpenWrt"),
		PropStrings(component, componentName),
	)

	configurations = Node("configurations", PropStrings("default", config_rel_str), target_comp)

	if device_tree_blob:
		images.append_node(
			Node(
				"fdt@" + str(fdtnum),
				PropStrings("description", arch_upper + " OpenWrt " + human_name + " device tree blob"),
				# data = /incbin/("{""" + str(device_tree_blob.relative_to(incbin)) + '''}"),
				PropStrings("type", "flat_dt"),
				PropStrings("arch", arch),
				PropStrings("compression", none),
				*checksum_algos,
			)
		)
		target_comp.append_prop(PropStrings("fdt", "fdt@" + str(fdtnum)))

	return Node("", PropStrings("description", arch_upper + " OpenWrt FIT (Flattened Image Tree)"), PropWords("#address-cells", 1), images, configurations)
