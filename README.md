# pycorsikaio [![CI](https://github.com/cta-observatory/pycorsikaio/actions/workflows/ci.yml/badge.svg)](https://github.com/cta-observatory/pycorsikaio/actions/workflows/ci.yml) [![PyPI version](https://badge.fury.io/py/corsikaio.svg)](https://badge.fury.io/py/corsikaio)


Python module to read the CORSIKA binary output files.

## Install

Run
```
pip install corsikaio
```

## Features

Load CORSIKA binary particle or cherenkov data files using python and numpy.

Also supports MMCS 6.5

```python
from corsikaio import CorsikaCherenkovFile
import matplotlib.pyplot as plt


with CorsikaCherenkovFile('cer000001') as f:
    print(f.run_header['run_number'])
    print(f.version)

    for e in f:
        print(e.header['total_energy'])
        
        plt.scatter(e.photons['x'], e.photons['y'])
        plt.show()
```



