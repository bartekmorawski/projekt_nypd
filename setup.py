import setuptools

setuptools.setup(
    name="NPDprojekt",
    version='1.0',
    license='BSD 2-clause',
    author="bartek morawski",
    packages=['nypd'],
    install_requires=['pandas', 'numpy', 'argparse', 'openpyxl']
)
