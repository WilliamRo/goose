from roma import console
from setuptools import setup


# Specify version
VERSION = '1.0.0.dev2'


# Preprocess
console.show_status('Running setup.py for goose-v' + VERSION + ' ...')
console.split('-')


# Run setup
def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='goose',
  packages=['goose'],
  install_requires=['py-roma'],
  version=VERSION,
  description='Gua Gua Gua!',
  long_description=readme(),
  long_description_content_type='text/markdown',
  author='William Ro',
  author_email='willi4m@zju.edu.cn',
  url='https://github.com/WilliamRo/goose',
  download_url='https://github.com/WilliamRo/goose/tarball/v' + VERSION,
  license='Apache-2.0',
  keywords=['cloud', 'distributed'],
  classifiers=[
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
  ],
)
