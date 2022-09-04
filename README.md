```
██████╗ ██╗   ██╗ █████╗ ██╗   ██╗██╗     ████████╗
██╔══██╗██║   ██║██╔══██╗██║   ██║██║     ╚══██╔══╝
██║  ██║██║   ██║███████║██║   ██║██║        ██║
██║  ██║╚██╗ ██╔╝██╔══██║██║   ██║██║        ██║
██████╔╝ ╚████╔╝ ██║  ██║╚██████╔╝███████╗   ██║
╚═════╝   ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝
```

***This ain't your daddy's configuration managment system***

Did you ever want to use substitution or includes in a congiguration language.  
Json won't do it, you have to bolt your own stuf on.  YAML offers anchors they 
are OK but to move to multiple files, you are now bolting your own stuf on.  
What about `python`?  We can just code our configuration in python! why not?


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

