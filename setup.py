import setuptools

setuptools.setup(
    name="beam-avro-testing",
    version=0.1,
    packages=setuptools.find_packages(),
    install_requires=['python-snappy', 'apache-beam[gcp]'])