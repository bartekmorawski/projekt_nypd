import setuptools

setuptools.setup(
    name="nypd",
    version='1.0',
    license='BSD 2-clause',
    author="bartek morawski",
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="./src"),
    install_requires=['pandas', 'numpy', 'argparse', 'openpyxl']
)
