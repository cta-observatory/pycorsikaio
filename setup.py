from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()


setup(
    name='corsikaio',
    version='0.2.3',
    description='Reader for corsika binary output files using numpy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/fact-project/corsikaio',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=find_packages(),
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    install_requires=[
        'numpy',
    ],
    zip_safe=False,
)
