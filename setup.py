from distutils.core import setup
import sys

setup (name              = 'pysubsonic',
       version           = '1.0',
       description       = 'pysubsonic - python client access to the Subsonic REST API',
       maintainer        = 'Vincent Batts',
       maintainer_email  = 'vbatts@hashbangbash.com',
       license           = 'MIT',
       long_description  = 'pysubsonic - python client access to the Subsonic REST API',
       url               = 'http://github.com/vbatts/pysubsonic',
       platforms         = ['Any'],
       packages          = ['pysubsonic'],
       py_modules        = [],
       scripts           = ['bin/subsonic'],
       package_dir       = {'': 'lib/'},
       )

