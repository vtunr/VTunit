#Building unity lib
add_library(unity STATIC vtunit/lib/unity/src/unity.c)
target_include_directories(unity PUBLIC vtunit/lib/unity/src)

#Including fff.h to our build
include_directories(vtunit/lib/fff/)
