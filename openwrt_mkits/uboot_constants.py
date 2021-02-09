__license__ = "GPL-2.0-or-later"

__copyright__ = """
(C) Copyright 2008 Semihalf

(C) Copyright 2000-2006
Wolfgang Denk, DENX Software Engineering, wd@denx.de.
"""

# https://github.com/u-boot/u-boot/blob/master/common/image.c

SUPPORTED_ARCHITECTURES = {"alpha", "arc", "arm", "arm64", "avr32", "blackfin", "i386", "ia64", "m68k", "microblaze", "mips", "mips64", "nds32", "nios2", "or1k", "powerpc", "ppc", "riscv", "s390", "sandbox", "sh", "sh", "sparc", "sparc64", "st200", "x86", "x86_64", "xtensa"}

SUPPORTED_COMPRESSIONS = {"none", "bzip2", "gzip", "lz4", "lzma", "lzo", "zstd"}

SUPPORTED_CHECKSUMS = {"crc32", "md5", "sha1"}

SUPPORTED_COMPONENTS = sorted(("aisimage", "standalone", "kernel", "kernel_noload", "ramdisk", "firmware", "script", "filesystem", "flat_dt", "gpimage", "kwbimage", "imximage", "imx8image", "imx8mimage", "invalid", "multi", "omapimage", "pblimage", "socfpgaimage", "socfpgaimage_v1", "ublimage", "mxsimage", "atmelimage", "x86_setup", "lpc32xximage", "rkimage", "rksd", "rkspi", "vybridimage", "zynqimage", "zynqmpimage", "zynqmpbif", "fpga", "tee", "firmware_ivt", "stm32image", "pmmc", "mtk_image", "copro", "sunxi_egon"))

SUPPORTED_OSES = {"invalid", "openbsd", "netbsd", "freebsd", "4_4bsd", "linux", "svr4", "esix", "solaris", "irix", "sco", "dell", "ncr", "lynxos", "vxworks", "psos", "qnx", "u_boot", "rtems", "unity", "integrity", "lynxos", "ose", "plan9", "tee", "u-boot", "openrtos", "opensbi", "efi"}
