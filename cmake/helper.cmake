#function to generate the test runner
function(init_test_runner)
    file(REMOVE_RECURSE ${CMAKE_SOURCE_DIR}/build_runner)
    file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/build_runner)
endfunction()

function(generate_test_runner array_c_file)
	foreach(dir ${array_c_file})
	  #file(RELATIVE_PATH FILE_PATH ${CMAKE_SOURCE_DIR} ${dir})
	  get_filename_component(FILE_NAME ${dir} NAME)
	  string(REPLACE .c _Runner.c RUNNER_NAME ${FILE_NAME})
	  execute_process(COMMAND python ${CMAKE_SOURCE_DIR}/vtunit/test_runner_generator.py --test_file ${dir})
	endforeach()
endfunction()

function(generate_mock test_file)
	get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
	execute_process(COMMAND pwd)
	execute_process(COMMAND python ../vtunit/parse.py --test_file ${test_file} --mock_prefix mock_ --include ${dirs})
endfunction()

init_test_runner()