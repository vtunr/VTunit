
import os
import argparse
from cmakelist_generator import *
from file_generator import *
import subprocess
from subprocess import check_output
import shutil
import re

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
        self.run_cmd(self.cmd_ninja_clean)
        os.chdir("../")
        
    def run_cmd(self, cmd):
        ret = subprocess.call(cmd, shell = True)
        if(ret):
            exit(ret)
    def cmake(self):
        try:
            os.mkdir("build")
        except:
            pass
        os.chdir("build")
        self.run_cmd(self.cmd_cmake)
        os.chdir("../")
    def list_test(self, filter):
        os.chdir("build")
        cmd = "ctest -N".split(" ")
        out = check_output(cmd)
        list_test = []
        for i in out.split("\n"):
            if("Test #" in i):
                splt = i.split(": ")[1].strip()
                if(filter):
                    result = re.match(filter, splt)
                    if(result):
                        list_test.append(splt)
                else:
                    list_test.append(splt)
        os.chdir("../")
        return list_test
    
    def print_test_list(self, filter):
        list_test = self.list_test(filter)
        len_test = len(list_test)
        print("%u test found :"%len_test)
        for test in list_test:
            print("\t %s"%test)

    def run(self, filter):
        if(filter != None):
            list_test = self.list_test(filter)
            if(not len(list_test)):
                raise Exception("No test found")
            os.chdir("build")
            for test in list_test:
                print("Building ... %s"%test)
                self.run_cmd(self.cmd_ninja+" test_"+test)
            self.run_cmd(self.cmd_ctest+" -R "+filter)
            self.run_cmd(self.cmd_gen_xml)
            os.chdir("../")
        else:
            os.chdir("build")
            self.run_cmd(self.cmd_ninja)
            self.run_cmd(self.cmd_ctest)
            self.run_cmd(self.cmd_gen_xml)
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
    build.add_argument('--run', help='Run unit test (can be filtered)', action='store_true')
    build.add_argument('--filter', help='Filter unit test')
    build.add_argument('--list', help='List unit test (can be filtered)', action='store_true')
    args = parser.parse_args()
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
        if(args.clean_all):
            pr.clean_all()
        if(args.cmake):
            pr.cmake()
        if(args.run):
            pr.run(args.filter)
        if(args.list):
            pr.print_test_list(args.filter)
if __name__ == '__main__':
    main()