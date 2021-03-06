import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [ Extension(
    "ucr",
    sources = ["ucr.pyx", "dtw.c"],
    depends = ["dtw.h"],
    include_dirs = [numpy.get_include()])
    ]

setup(
  name = 'UCR libraries for Python',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
