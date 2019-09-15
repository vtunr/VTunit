import os

class CMakeListsGenerator():
    def __init__(self, test_path = None):
        if(test_path == None):
            self.test_path = os.getcwd()
        else:
            self.test_path = test_path

    def isCMakeListsGen(self):
        return os.path.exists(os.path.join(self.test_path, "CMakeLists.txt"))
        
    def CreateCMakeLists(self):
        if(self.isCMakeListsGen()):
            raise Exception("Already created")
        else:
            self.genCMakeLists()

    def genCMakeLists(self):
        with open(os.path.join(self.test_path, "CMakeLists.txt"), 'w') as f:
            f.write("cmake_minimum_required(VERSION 2.6)\n\n")

            f.write("include(vtunit/cmake/ctest.cmake)\n")
            f.write("include(vtunit/cmake/helper.cmake)\n")
            f.write("include(vtunit/cmake/unity_fff.cmake)\n")
            f.write("include(include.cmake)\n")
            f.write("include(options.cmake)\n\n")

        with open(os.path.join(self.test_path, "include.cmake"), 'w') as f:
            f.write("# Here put your include folder \n\n")

        with open(os.path.join(self.test_path, "options.cmake"), 'w') as f:
            f.write("# Here put other options \n\n")

    def AddTest(self, test_cmake):
        with open(os.path.join(self.test_path, "CMakeLists.txt"), 'a') as f:
            f.write("include(test/%s)\n"%test_cmake)