# VTunit

This is a unit test/mock framework based on Unity and fff, aimed for embedded developers.

# Installation 

Clone this repository within the folder you want your unit test :

* `cd my_unit_test_folder`
* `git clone --recursive https://github.com/vtunr/VTunit.git vtunit`

If it's already in a git repository, you can add it as submodule :
* `git submodule add https://github.com/vtunr/VTunit.git {my_unit_test_folder}/vtunit`

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

* `cd my_unit_test_folder`
* `python vtunit/vtunit.py init`

# Creating a new unit test

* `cd my_unit_test_folder`
* `python vtunit/vtunit.py new --file_name {my_file_name.c}`

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

* `cd my_unit_test_folder`
* If you want to force calling cmake (need to be done once before calling `run`): `python vtunit/vtunit.py build --clean_all --cmake`
* Then to build and run : `python vtunit/vtunit.py build --run`
* To clean : `python vtunit/vtunit.py build --clean`

You can also filter the test you want to run :

* To list : `python vtunit/vtunit.py build --list --filter {my_regex}` (optional `--filter`)
* To filter : `python vtunit/vtunit.py build --run --filter {my_regex}`

You can also ignore prebuild/postbuild command by adding `--ignore_prebuild` and `--ignore_postbuild`

# TODO :

* Improve argparse
* Add setup.py so we don't have to clone it for each project
* Add possibility to run it in a docker container


