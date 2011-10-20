# -*- coding: utf-8 -*-
"""Setup per la llibreria de Switching"""
import os
import unittest
from distutils.command.clean import clean as _clean
from distutils.core import Command
from setuptools import setup

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

class Test(Command):
    """Passarem els tests unitaris que tinguem definits."""
    
    user_options  = []
    
    def initialize_options(self):
        """Inicialitzem."""
        pass
    
    def run(self):
        """Executem els tests."""
        import tests
        suite = unittest.TestLoader().loadTestsFromModule(tests.test_switching)
        unittest.TextTestRunner(verbosity=2).run(suite)
    
    def finalize_options(self):
        """Finalitzem."""
        pass

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
      cmdclass={'clean': Clean, 'test': Test})
      

