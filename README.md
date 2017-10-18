# pycorsikaio


Python module to read the CORSIKA binary output files.

## Install

Run
```
pip install https://github.com/fact-project/pycorsikaio/archive/master.tar.gz
```

## Features

Right now, only parsing of the run and event headers is supported,
as this was most urgently needed for e.g. calculation of effective
areas and sensitivity.
But we plan to add support for more subblock types in the future.

Because the output format changed with the CORSIKA versions, 
right now, only CORSIKA 6.5 and 7.56 are supported.


