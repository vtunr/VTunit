
import os
import argparse
from cmakelist_generator import *
from file_generator import *
import subprocess
import shutil
class Project:
    def __init__(self):
        self.current_folder = os.getcwd()
        self.cmake_gen = CMakeListsGenerator()
        self.define_command()

    def define_command(self):
        self.cmd_cmake = "cmake .. -GNinja"
        self.cmd_ninja =  "ninja"
        self.cmd_ctest = "ctest -V"
        self.cmd_gen_xml = "ruby ../vtunit/lib/unity/auto/parse_output.rb -xml Testing/Temporary/LastTest.log"
        self.cmd_ninja_clean = "ninja clean"


    def gen_project(self):
        if(self.cmake_gen.isCMakeListsGen()):
            #TODO : Update current config from command line
            raise Exception("Can't gen a project already init")
        self.cmake_gen.CreateCMakeLists()

    def create_new_unit_test(self, file_name, extra_include = None, test_folder = None):
        if(not self.cmake_gen.isCMakeListsGen()):
            raise Exception("Project not found")
        FG = FileGenerator(file_name, test_folder, extra_include, False)
        self.cmake_gen.AddTest("test_%s.cmake"%file_name[:-2])

    def clean_all(self):
        shutil.rmtree("build", ignore_errors=True)

    def clean(self):
        os.chdir("build")
        subprocess.call(self.cmd_ninja_clean, shell=True)
        os.chdir("../")

    def cmake(self):
        try:
            os.mkdir("build")
        except:
            pass
        os.chdir("build")
        subprocess.call(self.cmd_cmake, shell=True)
        os.chdir("../")

    def run(self):
        os.chdir("build")
        subprocess.call(self.cmd_ninja, shell=True)
        subprocess.call(self.cmd_ctest, shell=True)
        subprocess.call(self.cmd_gen_xml, shell=True)
        os.chdir("../")


def main():
    parser = argparse.ArgumentParser("VTunit")
    subparser = parser.add_subparsers(dest='command')
    init = subparser.add_parser('init', help='Init project')
    create_test = subparser.add_parser('new', help='Create new unit test')
    create_test.add_argument("--file_name",
        help='C File name to test'
    )
    create_test.add_argument("--extra_include",
        help='New include to add for this test'
    )
    create_test.add_argument("--test_folder",
        help='Where to generate the files'
    )
    build = subparser.add_parser('build', help='Build things')
    build.add_argument('--clean', help='Clean unit test (Ninja)', action='store_true')
    build.add_argument('--clean_all', help='Clean all unit test (CMake+Ninja)', action='store_true')
    build.add_argument('--cmake', help='Run cmake', action='store_true')
    build.add_argument('--run', help='Run unit test', action='store_true')
    args = parser.parse_args()
    print(args)
    pr = Project()
    if(args.command == "init"):
        print "Generating project"
        pr.gen_project()
    if(args.command == "new"):
        if(args.extra_include or args.test_folder):
            raise Exception("Not supported options")
        pr.create_new_unit_test(args.file_name)
    if(args.command == "build"):
        if(args.clean):
            pr.clean()
        if(args.command):
            pr.clean_all()
        if(args.command):
            pr.cmake()
        if(args.command):
            pr.run()
if __name__ == '__main__':
    main()