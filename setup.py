#!/usr/bin/env python

from distutils.core import setup
from glob import glob


setup(name='Templater',
      version='1.1.2',
      description='Creates file from templates',
      author='Alexander Weigl',
      author_email='alexweigl@gmail.com',
      url='http://areku.kilu.de',
      package_dir={'':'src'},
      scripts=['src/templater'],
      py_modules=['tplinput'],
      provides=['tplinput (1.0)'],

      data_files=[
#        ('templater'      ,'defaults')),
        ('templater/tpl.d',glob('data/tpl.d/**')),
        ]
     )
