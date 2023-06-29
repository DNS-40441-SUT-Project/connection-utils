import setuptools

setuptools.setup(
    include_package_data=True,
    name='connection_utils',
    version='0.2.1',
    packages=setuptools.find_packages(),
    install_requires=['rsa', ],
)
