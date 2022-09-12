from setuptools import (setup, find_packages)
from os import path

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='dvault',
      version=open(path.join(path.dirname(__file__),"VERSION")).read().rstrip(),
      description='make that money grow',
      url='https://github.com/AlwaysTraining/dvault',
      author='Derrick Karimi',
      author_email='derrick.karimi@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_dir={'dvault': 'dvault'},
      #scripts=['dvault/dvault'],
      entry_points = {
          'console_scripts': [
              'dvault=dvault.__main__:main',
              ]
          },
      install_requires=requirements,
      zip_safe=False,
      scripts=['venv_launch.sh', 'dvault_service_status.sh']
      )
