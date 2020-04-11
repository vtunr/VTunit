function(generate_test_runner test_file)
	#file(RELATIVE_PATH FILE_PATH ${CMAKE_SOURCE_DIR} ${dir})
	get_filename_component(FILE_NAME ${test_file} NAME)
	string(REPLACE .c _Runner.c RUNNER_NAME ${FILE_NAME})
	add_custom_command(OUTPUT 
		test_runner/${RUNNER_NAME}
	COMMAND python2 ${CMAKE_SOURCE_DIR}/vtunit/generator/test_runner_generator.py --test_file ${test_file}
	DEPENDS ${test_file}
)
endfunction()

function(generate_mock test_file)
	get_filename_component(FILE_NAME ${test_file} NAME)
	string(REPLACE .c " " FILE_NAME ${FILE_NAME})
	string(STRIP ${FILE_NAME} FILE_NAME)
	get_property(dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY INCLUDE_DIRECTORIES)
	add_custom_target(mock_${FILE_NAME} COMMAND python2 ../vtunit/generator/mock_generator.py --test_file ${test_file} --mock_prefix mock_ --include ${dirs})
	add_dependencies(${FILE_NAME} mock_${FILE_NAME})
endfunction()


list(APPEND PREBUILD_CMD echo Running PREBUILD)
list(APPEND POSTBUILD_CMD echo Running POSTBUILD)
function(define_prebuild)
	message(STATUS "Prebuild is ${PREBUILD_CMD}")
	add_custom_target(prebuild ${PREBUILD_CMD})
endfunction()

function(define_postbuild)
	add_custom_target(postbuild ${POSTBUILD_CMD})
endfunction()