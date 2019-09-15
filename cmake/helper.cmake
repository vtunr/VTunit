#function to generate the test runner
function(init_test_runner)
    file(REMOVE_RECURSE ${CMAKE_SOURCE_DIR}/build_runner)
    file(MAKE_DIRECTORY ${CMAKE_SOURCE_DIR}/build_runner)
endfunction()

function(generate_test_runner test_file)
	#file(RELATIVE_PATH FILE_PATH ${CMAKE_SOURCE_DIR} ${dir})
	get_filename_component(FILE_NAME ${test_file} NAME)
	string(REPLACE .c _Runner.c RUNNER_NAME ${FILE_NAME})
	add_custom_command(OUTPUT test_runner/${RUNNER_NAME}
	COMMAND python ${CMAKE_SOURCE_DIR}/vtunit/generator/test_runner_generator.py --test_file ${test_file})
endfunction()

function(generate_mock test_file)
	get_filename_component(FILE_NAME ${test_file} NAME)
	string(REPLACE .c " " FILE_NAME ${FILE_NAME})
	string(STRIP ${FILE_NAME} FILE_NAME)
	get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
	add_custom_target(mock_${FILE_NAME} COMMAND python ../vtunit/generator/mock_generator.py --test_file ${test_file} --mock_prefix mock_ --include ${dirs})
	add_dependencies(${FILE_NAME} mock_${FILE_NAME})
endfunction()

init_test_runner()