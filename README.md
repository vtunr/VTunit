# VTunit

This is a unit test/mock framework based on Unity and fff, aimed for embedded developer.
All command can be done over docker, and this the main way of working.

# Installation 

Clone this repository with in the folder you want your unit test :

* `cd my_unit_test_folder`
* `git clone --recursive https://github.com/vtunr/VTunit.git vtunit`

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

You can also add include in `CMakeLists.txt`

# Running a new test
 
Not in this script yet.

# TODO :

* Add include.cmake & option.cmake to CMakeLists when generating it
* Add run/build/clean in vtunit script
* Add setup.py so we don't have to clone it for each project


