from os import path
from setuptools import setup

with open(path.join(path.dirname(path.abspath(__file__)), 'README.rst')) as f:
    readme = f.read()

setup(
    name             = 'libav',
    version          = '0.1',
    description      = 'Convert, manipulate and stream a variety of multimedia formats.',
    long_description = readme,
    author           = 'slegendr',
    author_email     = 'slegendr@redhat.com',
    url              = 'http://wiki',
    packages         = ['libav'],
    install_requires = ['chrisapp'],
    test_suite       = 'nose.collector',
    tests_require    = ['nose'],
    license          = 'MIT',
    zip_safe         = False,
    python_requires  = '>=3.6',
    entry_points     = {
        'console_scripts': [
            'libav = libav.__main__:main'
            ]
        }
)
