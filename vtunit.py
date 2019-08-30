
import os
import argparse
from cmakelist_generator import *
from file_generator import *

class Project:
    def __init__(self):
        self.current_folder = os.getcwd()
        self.cmake_gen = CMakeListsGenerator()
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
    args = parser.parse_args()
    pr = Project()
    if(args.command == "init"):
        print "Generating project"
        pr.gen_project()
    if(args.command == "new"):
        if(args.extra_include or args.test_folder):
            raise Exception("Not supported options")
        pr.create_new_unit_test(args.file_name)

if __name__ == '__main__':
    main()