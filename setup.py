import os
import sys
from setuptools import setup

# Get the installation dir and version from command line
install_dir = "/opt/helloservice/"
version = "0.1.0"

for argument in sys.argv:
    if argument.startswith("--install-dir"):
        install_dir = argument.split("=")[1]
        # remove it. setup doesn't need it.
        sys.argv.remove(argument)

for argument in sys.argv:
    if argument.startswith("--version"):
        version = argument.split("=")[1]
        # remove it. setup doesn't need it.
        sys.argv.remove(argument)

with open('README.md', 'r') as rf:
    long_description = rf.read()


def get_data_files() -> list:
    data_files = [(install_dir + '/meta-info', ['README.md'])]
    return data_files


def get_packages() -> list:
    ignore_list = ['test', '__pycache__']
    packages = ['hello']
    package_root = 'hello'
    for root, directories, _ in os.walk(package_root):
        for a_dir in directories:
            package = root + '/' + a_dir
            package = package.replace('/', '.')
            print(set(package.split('.')), set(ignore_list))
            if len(set(package.split('.')).intersection(set(ignore_list))) == 0:
                packages.append(package)
    return packages


setup(name='HelloService',
      version=version,
      url='https://github.com/ajayksri/hellogene',
      license='',
      author='Ajay Srivastava',
      author_email='ajay.ksri@gmail.com',
      description='Technology show case',
      package_dir={'hello': 'hello'},
      packages=get_packages(),
      package_data={
        'hello': ['py.typed'],
      },
      data_files=get_data_files(),
      long_description=long_description,
      zip_safe=False,
      python_requires='>=3.6')
