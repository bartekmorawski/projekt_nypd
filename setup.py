import setuptools

setuptools.setup(
    name="nypd_projekt",
    author="bartek morawski",
    packages=setuptools.find_packages(),
    install_requirements=['pandas', 'numpy', 'argparse', 'os', 'openpyxl', 'warnings']
)
