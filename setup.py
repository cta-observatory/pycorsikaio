from setuptools import setup, find_packages


setup(
    name='corsikaio',
    version='0.1.0',
    description='Reader for corsika binary output files using numpy',
    url='http://github.com/fact-project/corsikaio',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    zip_safe=False,
)
