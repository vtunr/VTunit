#Building unity lib
add_library(unity STATIC ${VT_LIB}/unity/src/unity.c)
target_include_directories(unity PUBLIC ${VT_LIB}/unity/src)

#Including fff.h to our build
include_directories(${VT_LIB}/fff/)
