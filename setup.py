import setuptools

setuptools.setup(
    name="NPDprojekt",
    version='1.0',
    license='BSD 2-clause',
    author="bartek morawski",
    packages=setuptools.find_packages('src/'),
    install_requires=['pandas', 'numpy', 'argparse', 'openpyxl']
)
