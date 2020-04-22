[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=vtunr_VTunit&metric=alert_status)](https://sonarcloud.io/dashboard?id=vtunr_VTunit)
[![Docker](https://img.shields.io/docker/v/vtunr/vtunit?logo=docker)](https://hub.docker.com/repository/docker/vtunr/vtunit)

# VTunit

This is a unit test/mock framework based on Unity and fff, aimed for embedded developers.

# Installation 

## Local use

### Installing vtunit

Install the package with pip

* `pip install git+https://github.com/vtunr/VTunit.git#egg=VTunit`
* `pip install -e .` if you clone the repository (for development purpose)

### Package requirements 

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

## Docker

There is one docker image available on [dockerhub](https://hub.docker.com/repository/docker/vtunr/vtunit/general)

You can use to run test directly in docker : 

```
docker run --name vtunit --rm -v ${PWD}:/project -v /project/ -t vtunr/vtunit:latest vtunit unit_test/ build --cmake --run
```

You can also run it interactively :
```
docker run --name vtunit --rm -v ${PWD}:/project -v /project/ -it vtunr/vtunit:latest
```

and then run your commands : 
```
root@56f7875b6a45:/project# vtunit unit_test/ build --clean_all --cmake --run
Running cmake /project/unit_test -GNinja
...
```

# Setup unit test for a project

* `vtunit {path_unit_test} init`

# Creating a new unit test

* `vtunit {path_unit_test} new --file_name {my_file_name.c}`

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

* If you want to force calling cmake (need to be done once before calling `run`): `vtunit {path_unit_test} build --clean_all --cmake`
* Then to build and run : `vtunit {path_unit_test} build --run`
* To clean : `vtunit {path_unit_test} build --clean`

You can also filter the test you want to run :

* To list : `vtunit {path_unit_test} build --list --filter {my_regex}` (optional `--filter`)
* To filter : `vtunit {path_unit_test} build --run --filter {my_regex}`

You can also ignore prebuild/postbuild command by adding `--ignore_prebuild` and `--ignore_postbuild`


# TODO :

* Improve argparse
* Adding subproject
* Using pypi
* Making a proper release on pypi & dockerhub


