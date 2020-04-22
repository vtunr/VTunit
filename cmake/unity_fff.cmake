#Building unity lib
add_library(unity STATIC vtunit_files/lib/unity/src/unity.c)
target_include_directories(unity PUBLIC vtunit_files/lib/unity/src)

#Including fff.h to our build
include_directories(vtunit_files/lib/fff/)
