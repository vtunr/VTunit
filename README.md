[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=vtunr_VTunit&metric=alert_status)](https://sonarcloud.io/dashboard?id=vtunr_VTunit)

# VTunit

This is a unit test/mock framework based on Unity and fff, aimed for embedded developers.

# Installation 

Install the package with pip

* `pip install -e git+https://github.com/vtunr/VTunit.git#egg=VTunit`
* `pip install -e .` if you clone the repository (for development purpose)

## Package to install (if you choose local build)

On ubuntu/WSL :

* `sudo apt-get install cmake ninja-build ruby`
* You'll also need `universal_ctag` :
```
git clone https://github.com/universal-ctags/ctags.git
cd ctags
./autogen.sh 
./configure
make
sudo make install
``` 

# Setup unit test for a project

* `python -m  vtunit {path_unit_test} init`

# Creating a new unit test

* `python -m vtunit {path_unit_test} new --file_name {my_file_name.c}`

It will generate into the test folder:
* `test_{file_to_test}.c`
* `test_{file_to_test}.cmake`

You then need to add the c file you want to compile for your test in the `test_{file_to_test}.cmake`.

You can also add include in `include.cmake`

# Automatic mocking

You can automatically mock header.

You just need to add `mock_` prefix to the header you want to include :

`#include "mock_my_header.h"`

`#include "mock_my_folder/my_header.h"`

# Prebuild / Postbuild

There is a way to run command before and after build (not after run)

You need to add :

* `list(APPEND PREBUILD_CMD && cmd_you_want)` in `prebuild.cmake`
* `list(APPEND POSTBUILD_CMD && cmd_you_want)` in `postbuild.cmake`

# Running test

Running in WSL or linux : 

* If you want to force calling cmake (need to be done once before calling `run`): `python -m vtunit {path_unit_test} build --clean_all --cmake`
* Then to build and run : `python -m vtunit {path_unit_test} build --run`
* To clean : `python -m vtunit {path_unit_test} build --clean`

You can also filter the test you want to run :

* To list : `python -m vtunit {path_unit_test} build --list --filter {my_regex}` (optional `--filter`)
* To filter : `python -m vtunit {path_unit_test} build --run --filter {my_regex}`

You can also ignore prebuild/postbuild command by adding `--ignore_prebuild` and `--ignore_postbuild`

# TODO :

* Improve argparse
* Add possibility to run it in a docker container


