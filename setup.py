import setuptools

setuptools.setup(
    name="nypd_projekt",
    version='1.0',
    license='BSD 2-clause',
    author="bartek morawski",
    packages=setuptools.find_packages(),
    install_requires=['pandas', 'numpy', 'argparse', 'openpyxl']
)
