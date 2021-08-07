import setuptools

setuptools.setup(
    name="iht-profiling-beam-summit-2021",
    version=0.1,
    packages=setuptools.find_packages(),
    install_requires=['python-snappy', 'apache-beam[gcp]'])