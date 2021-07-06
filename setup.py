from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()


extras = {
    'zstd': ['zstandard'],
    'tests': ['pytest'],
}
extras['all'] = list({dep for deps in extras.values() for dep in deps})

setup(
    name='corsikaio',
    description='Reader for corsika binary output files using numpy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://github.com/cta-observatory/corsikaio',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    license='MIT',
    packages=find_packages(),
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
    extras_require=extras,
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
    zip_safe=False,
)
