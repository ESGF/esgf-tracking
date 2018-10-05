# PUB SIM

An ESGF Publication Simulator

The current simulator is pub-sim-2.py

Usage:  python pub-sim-2.py <list-file> <count> <interval>

<list-file> is a list of paths that includes the dataset version number.  cmip6-test-wvs.txt has an example of the format.

<count> of publication  
<interval time between the start of each publication.

Example.  (base)$ python pub-sim-2.py cmip6-test-wvs.txt 16 30

Will publish 16 datasets, one every 30 seconds.
