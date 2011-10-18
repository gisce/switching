# -*- coding: utf-8 -*-
"""Setup per la llibreria de Switching"""
import os

from switching import __version__

PACKAGES = ['switching']
PACKAGES_DATA = {}

class Clean(_clean):
    """Eliminem el directory build i els bindings creats."""
    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print "Cleaning %s dir" % self.build_base
            shutil.rmtree(self.build_base)

"""__FILE__ per obtenir el path dels fitxers data(xsd)"""
setup(name='switching',
      description='Llibreria de switching',
      author='GISCE Enginyeria',
      author_email='devel@gisce.net',
      url='http://www.gisce.net',
      version=__version__,
      license='General Public Licence 2'
      long_description='''Long description''',
      provides=['switching'],
      install_requires=[],      
      packages=PACKAGES,  
      package_data=PACKAGES_DATA,
      cmdclass={'clean': Clean})
      

