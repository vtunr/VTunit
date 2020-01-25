import os

class CMakeListsGenerator():
    def __init__(self, test_path = None):
        self.name_cmake = "CMakeLists.txt"
        if(test_path == None):
            self.test_path = os.getcwd()
        else:
            self.test_path = test_path

    def isCMakeListsGen(self):
        return os.path.exists(os.path.join(self.test_path, self.name_cmake))
        
    def CreateCMakeLists(self):
        if(self.isCMakeListsGen()):
            raise Exception("Already created")
        else:
            self.genCMakeLists()

    def genCMakeLists(self):
        with open(os.path.join(self.test_path, self.name_cmake), 'w') as f:
            f.write("cmake_minimum_required(VERSION 2.6)\n\n")

            f.write("include(vtunit/cmake/ctest.cmake)\n")
            f.write("include(vtunit/cmake/helper.cmake)\n")
            f.write("include(vtunit/cmake/unity_fff.cmake)\n")
            f.write("include(include.cmake)\n")
            f.write("include(options.cmake)\n\n")
            f.write("include(prebuild.cmake)\n")
            f.write("include(postbuild.cmake)\n")
            f.write("define_prebuild()\n")
            f.write("define_postbuild()\n\n")

        with open(os.path.join(self.test_path, "include.cmake"), 'w') as f:
            f.write("# Here put your include folder \n\n")

        with open(os.path.join(self.test_path, "options.cmake"), 'w') as f:
            f.write("# Here put other options \n\n")

        with open(os.path.join(self.test_path, "prebuild.cmake"), 'w') as f:
            f.write("# Here put your prebuild cmd\n\n")

        with open(os.path.join(self.test_path, "postbuild.cmake"), 'w') as f:
            f.write("# Here put your postbuild cmd\n\n")

    def AddTest(self, test_cmake):
        with open(os.path.join(self.test_path, self.name_cmake), 'a') as f:
            f.write("include(test/%s)\n"%test_cmake)