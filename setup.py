#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name="barcode",
      version="1.0",
      description="Python Bindings for the GNU Barcode Library",
      author="Max Dornseif",
      author_email="md@hudora.de",
      url="http://c0re.jp/",
      ext_modules=[Extension("barcode", ["barcodemodule.c"],
                             libraries=["barcode"],
                             # define_macros=[('DEBUG', '1')],
                             extra_compile_args=['-Ibarcode-0.98'],
                             extra_link_args=['-Lbarcode-0.98']
                             )]) 
     

