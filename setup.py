# -*- coding: utf-8 -*-
"""Setup per la llibreria de Switching"""
import os
from distutils.command.clean import clean as _clean
from distutils.core import setup

from switching import __version__

PACKAGES = ['switching', 'switching.messages']
PACKAGES_DATA = {'switching': ['data/*.xsd']}

class Clean(_clean):
    """Eliminem el directory build i els bindings creats."""
    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print "Cleaning %s dir" % self.build_base
            shutil.rmtree(self.build_base)

setup(name='switching',
      description='Llibreria de switching',
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version=__version__,
      license='General Public Licence 2',
      long_description='''Long description''',
      provides=['switching'],
      install_requires=['lxml'],      
      packages=PACKAGES,  
      package_data=PACKAGES_DATA,
      scripts=[],
      cmdclass={'clean': Clean})
      

