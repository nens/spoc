from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django >= 1.6',
    'django-celery',
    'django-extensions',
    'django-nose',
    'django-jsonfield',
    'gunicorn',
    'python-memcached',
    'werkzeug',
    'djangorestframework',
    'south',
    'markdown',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='spoc',
      version=version,
      description="Single Point Of Configuration (fews)",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='alexandr.seleznev',
      author_email='alexandr.seleznev@nelen-schuurmans.nl',
      url='https://github.com/nens/spoc',
      license='GPL',
      packages=['spoc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
