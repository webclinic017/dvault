```
██████╗ ██╗   ██╗ █████╗ ██╗   ██╗██╗     ████████╗
██╔══██╗██║   ██║██╔══██╗██║   ██║██║     ╚══██╔══╝
██║  ██║██║   ██║███████║██║   ██║██║        ██║
██║  ██║╚██╗ ██╔╝██╔══██║██║   ██║██║        ██║
██████╔╝ ╚████╔╝ ██║  ██║╚██████╔╝███████╗   ██║
╚═════╝   ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
```

***This ain't your daddy's configuration managment system***

Buy, using a bracket order a list of tickers for a given bet size


## Development environment
### How I setup my development python env
```
python3 -m venv dvault_venv
. dvault_venv/bin/activate
pip install wheel
```

### Get the Source
```
git clone git@github.com:AlwaysTraining/dvault.git
cd dvault
```

### How to do a full rebuild
```
pip uninstall -y dvault
python setup.py bdist_wheel
pip install dist/*.whl
```

## Dependencies API Reference
- https://github.com/alpacahq/alpaca-trade-api-python/

