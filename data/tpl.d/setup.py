<%
from tplinput  import cread, TextInput, Line, LongTextInput      

name, version, author, author_email, desc, scripts, modules, provides, long_desc  = cread (
    Line('Input the values for the setup.py file'),
    TextInput('Progammename:'),
    TextInput('Version:'),
    TextInput('Auhtor', 'Alexander Weigl'),
    TextInput('E-Mail', 'alexweigl@gmail.com'),
    TextInput('Beschreibung'),
    TextInput('Scripts'),
    TextInput('Modules'),
    LongTextInput('Provides [Jede Zeile: funktion (version)]'),
    LongTextInput('Lange Beschreibung')

)

implode = lambda x: "'"+("','".join(x))+"'"

scripts = implode(scripts.split(' '))
modules = implode(modules.split(' '))
provides = implode(provides.split("\n"))
%>
#!/usr/bin/env python

from distutils.core import setup

setup(name='${name}',
      version='${version}',
      description='${desc}',
      author='${author}',
      author_email='${author_email}',
      url='http://areku.kilu.de',
      download_url='',
      maintainer = None,
      maintainer_email = None,
      scripts=[${scripts}],
      py_modules=[${modules}],
      provides=[${provides}],

      classifiers=[ # see http://pypi.python.org/pypi?%3Aaction=list_classifiers for all !
#        'Development Status :: 4 - Beta',
#        'Environment :: Console',
#        'Environment :: Web Environment',
#        'Intended Audience :: End Users/Desktop',
#        'Intended Audience :: Developers',
#        'Intended Audience :: System Administrators',
#        'License :: OSI Approved :: Python Software Foundation License',
#        'Operating System :: MacOS :: MacOS X',
#        'Operating System :: Microsoft :: Windows',
#        'Operating System :: POSIX',
#        'Programming Language :: Python',
#        'Topic :: Communications :: Email',
#        'Topic :: Office/Business',
#        'Topic :: Software Development :: Bug Tracking',
        ],      
      long_description="""${long_desc}""",
     )
