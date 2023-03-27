# pycorsikaio [![CI](https://github.com/cta-observatory/pycorsikaio/actions/workflows/ci.yml/badge.svg)](https://github.com/cta-observatory/pycorsikaio/actions/workflows/ci.yml) [![PyPI version](https://badge.fury.io/py/corsikaio.svg)](https://badge.fury.io/py/corsikaio)


Python module to read the CORSIKA binary output files.

## Install

Run
```
pip install corsikaio
```

## Features

### Simple native reading

Load CORSIKA binary particle or Cherenkov data files using python and numpy.

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

### Astropy table

> **Note**
> You need to install ``astropy`` along _pycorsikaio_ to use this feature.

```python
from corsikaio.reader import CorsikaReader

input_corsika_file = "DAT00001"

reader = CorsikaReader(
    input_corsika_file,
    max_events=5,
    load_run_headers=False,
    load_event_headers=False,
    load_particles=True,
    load_longitudinal=False,
    load_event_ends=False,
    load_run_ends=False,
    selected_keys=["event_number", "particle_description", "x", "y"],
)

table = reader.read()
```

