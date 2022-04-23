import pkg_resources

from setuptools import find_packages
from setuptools import setup

with open('requirements.txt', 'r') as fh:
    reqs = [str(requirement)
            for requirement in pkg_resources.parse_requirements(fh)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyhup',
    version='0.0.1',
    url='https://github.com/hearai/parse-hamnosys.git',
    author='Palntykow, M., Olech, M., Majchrowska, S.',
    description='pyhup is a Python library for '
                'HamNoSys Universal Parsing',
    long_description=long_description,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=reqs,
)
