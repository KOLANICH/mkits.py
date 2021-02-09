from ast import literal_eval
from plumbum import cli
from fdt import FDT

from . import genITS, __copyright__, DEFAULT_CHECKSUM_ALGOS
from .uboot_constants import SUPPORTED_OSES, SUPPORTED_ARCHITECTURES, SUPPORTED_CHECKSUMS, SUPPORTED_COMPRESSIONS, SUPPORTED_COMPONENTS


class CLI(cli.Application):
	kernel_ver = cli.SwitchAttr(["-v", "--kernel-version"], mandatory=True, help="set kernel version to 'version'")
	kernel_image = cli.SwitchAttr(["-k", "--kernel"], cli.ExistingFile, mandatory=True, help="include kernel image 'kernel'")
	arch = cli.SwitchAttr(["-A", "--architecture"], cli.Set(*SUPPORTED_ARCHITECTURES), mandatory=True, help="set architecture to 'arch'")
	config = cli.SwitchAttr(["-c", "--config"], mandatory=True, help="set config name 'config'")
	load_addr = cli.SwitchAttr(["-a", "--base"], str, mandatory=True, help="set load address to 'addr' (hex)")
	entry_addr = cli.SwitchAttr(["-e", "--entry-point"], str, mandatory=True, help="set entry point to 'entry' (hex)")

	fdtnum = cli.SwitchAttr(["-n", "--unit-address"], int, help="fdt unit-address 'address'", default=1)

	component = cli.SwitchAttr(["--component"], cli.Set(*SUPPORTED_COMPONENTS), default="kernel")
	compression = cli.SwitchAttr(["-C", "--compression"], cli.Set(*SUPPORTED_COMPRESSIONS), default="lzma", help="set compression type 'comp'")
	checksumAlgos = cli.SwitchAttr(["--checksum-algos"], cli.Set(*SUPPORTED_CHECKSUMS, csv=True), help="Algorithms to use in checksum", default=DEFAULT_CHECKSUM_ALGOS)
	os_name = cli.SwitchAttr(["-O", "--osname"], cli.Set(*SUPPORTED_OSES), help="set operating system to 'os'", default="linux")

	its_file = cli.SwitchAttr(["-o", "--output"], help="create output file 'its_file'", default="-")

	device_tree_blob = cli.SwitchAttr(["-d", "--dtb"], cli.ExistingFile, help="include Device Tree Blob 'dtb'", default=None)
	human_name = cli.SwitchAttr(["-D", "--human-name"], help="human friendly Device Tree Blob 'name'")

	def main(self):
		self.kernel_image = Path(self.kernel_image).absolute()
		self.config = Path(self.config).absolute()

		if self.device_tree_blob:
			self.device_tree_blob = Path(self.device_tree_blob).absolute()

		self.load_addr = literal_eval(self.load_addr)
		self.entry_addr = literal_eval(self.entry_addr)

		resNode = genITS(self.arch, self.os_name, self.kernel_image, self.kernel_ver, self.load_addr, self.entry_addr, self.config, self.fdtnum, self.compression, self.checksumAlgos, human_name=self.human_name, device_tree_blob=self.device_tree_blob, component=self.component)

		res = FDT()
		res.root = resNode
		res = res.to_dts()

		if self.its_file == "-":
			print(res)
		else:
			Path(self.its_file).write_text(res)


if __name__ == "__main__":
	CLI.run()
