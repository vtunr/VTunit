
import os 

class FileGenerator():
    def __init__(self, c_file_name, test_dest = None, extra_include = None, static = False):
        self.c_file_name = c_file_name
        if(test_dest == None):
            self.test_dest = os.path.join(os.getcwd(), "test")
        else:
            self.test_dest = test_dest
        if(not os.path.exists(self.test_dest)):
            os.makedirs(self.test_dest)
        self.extra_include = extra_include
        self.static = static
        self.test_file_name = self.getTestFileName()
        self.generate_test_c_file()
        self.generate_test_cmake_file()

    def getTestFileName(self):
        return "test_"+self.c_file_name[:-2]

    def generate_test_c_file(self):
        with open(os.path.join(self.test_dest, self.test_file_name)+".c", 'w') as f:
            f.write("#include \"unity.h\"\n")
            f.write("#include \"fff.h\"\n\n")
            f.write("DEFINE_FFF_GLOBALS\n\n")
            f.write("void setUp(void)\n")
            f.write("{\n\n")
            f.write("}\n\n")
            f.write("void tearDown(void)\n")
            f.write("{\n\n")
            f.write("}\n\n")

    def generate_test_cmake_file(self):
        with open(os.path.join(self.test_dest, self.test_file_name)+".cmake", 'w') as f:
            f.write("set(FILE_TESTED %s)\n"%self.c_file_name[:-2])
            f.write("set(TEST_FILE test/test_${FILE_TESTED}.c)")
            f.write("generate_test_runner(${TEST_FILE})\n\n")
            f.write("add_executable(test_${FILE_TESTED}\n")
            f.write("   ${TEST_FILE}\n")
            f.write("   build/test_runner/test_${FILE_TESTED}_Runner.c\n")
            f.write(")\n\n")
            f.write("generate_mock(${TEST_FILE})\n")
            f.write("target_include_directories(test_${FILE_TESTED} PUBLIC ${CMAKE_SOURCE_DIR}/build/mock/test_${FILE_TESTED}/)\n\n")
            f.write("target_link_libraries(test_${FILE_TESTED} unity)\n")
            f.write("add_test(${FILE_TESTED} test_${FILE_TESTED})")