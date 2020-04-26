
from subprocess import check_output
import pkg_resources
import subprocess
import argparse
import shutil
import sys
import os
import re
from generator.cmakelist_generator import *
from generator.file_generator import *


class Project:
    def __init__(self, dir):
        self.project_folder = os.path.realpath(dir)
        self.vtunit_folder = os.path.realpath(os.path.dirname(__file__))
        self.vtunit_cmakehelper_folder = os.path.join(self.vtunit_folder, "cmake")
        self.vtunit_lib_folder = os.path.join(self.vtunit_folder, "lib")
        try:
            os.makedirs(os.path.join(self.project_folder))
        except OSError:
            pass
        os.chdir(self.project_folder)
        self.cmake_gen = CMakeListsGenerator(self.project_folder)
        self.define_command()

    def define_command(self):
        self.cmd_cmake = "cmake %s -GNinja -DVT_CMAKEHELPER=%s -DVT_LIB=%s"%(self.project_folder, self.vtunit_cmakehelper_folder, self.vtunit_lib_folder)
        self.cmd_ninja =  "ninja"
        self.cmd_ctest = "ctest -V"
        self.cmd_gen_xml = "vtunit_output_generator --log_file Testing/Temporary/LastTest.log --junit_xml"
        self.cmd_ninja_clean = "ninja clean"
        self.cmd_prebuild = "ninja prebuild"
        self.cmd_postbuild = "ninja postbuild"

    def gen_project(self, name):
        if(self.cmake_gen.is_cmakelists_generated()):
            #TODO : Update current config from command line
            raise Exception("Can't gen a project already init")
        self.cmake_gen.create_cmakelists(name)

    def create_new_unit_test(self, file_name, extra_include = None, test_folder = None):
        if(not self.cmake_gen.is_cmakelists_generated()):
            raise Exception("Project not found")
        FileGenerator(file_name, test_folder, extra_include, False)
        self.cmake_gen.add_test("test_%s.cmake"%file_name[:-2])

    def clean_all(self):
        shutil.rmtree("build", ignore_errors=True)

    def clean(self):
        os.chdir("build")
        self.run_cmd(self.cmd_ninja_clean)
        os.chdir("../")

    def run_cmd(self, cmd, ignore_error = False):
        print("Running %s"%cmd)
        ret = subprocess.call(cmd, shell = True)
        if(ret and not ignore_error):
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
            test_splt = i.split(": ")
            if(len(test_splt)>1 and test_splt[0].strip().startswith("Test")):
                splt = test_splt[1].strip()
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

    def run(self, filter, ignore_postbuild, ignore_prebuild):
        if(not ignore_prebuild):
            try:
                os.chdir("build")
            except OSError:
                self.cmake()
                os.chdir("build")
            self.run_cmd(self.cmd_prebuild)
            os.chdir("../")
        if(filter != None):
            list_test = self.list_test(filter)
            if(not len(list_test)):
                raise Exception("No test found")
            os.chdir("build")
            for test in list_test:
                print("Building ... %s"%test)
                self.run_cmd(self.cmd_ninja+" test_"+test)
            if(not ignore_postbuild):
                self.run_cmd(self.cmd_postbuild)
            self.run_cmd(self.cmd_ctest+" -R "+filter, True)
            self.run_cmd(self.cmd_gen_xml)
            os.chdir("../")
        else:
            os.chdir("build")
            self.run_cmd(self.cmd_ninja)
            if(not ignore_postbuild):
                self.run_cmd(self.cmd_postbuild)
            self.run_cmd(self.cmd_ctest, True)
            self.run_cmd(self.cmd_gen_xml)
            os.chdir("../")


def process_build(pr, args):
    if(args.clean):
        pr.clean()
    if(args.clean_all):
        pr.clean_all()
    if(args.cmake):
        pr.cmake()
    if(args.run):
        pr.run(args.filter, args.ignore_postbuild, args.ignore_prebuild)
    if(args.list):
        pr.print_test_list(args.filter)

def process_new(pr, args):
    pr.create_new_unit_test(args.file_name)

def process_init(pr, name):
    print("Generating project")
    pr.gen_project(name)

def main():
    parser = argparse.ArgumentParser("VTunit")
    parser.add_argument('--version', '-v', action='version', version = pkg_resources.require("VTunit")[0].version)
    parser.add_argument('project_path', nargs='?', default=os.getcwd())
    subparser = parser.add_subparsers(dest='command')
    init = subparser.add_parser('init', help='Init project')
    init.add_argument("--name", default = "unit test", help="Name of the project")
    create_test = subparser.add_parser('new', help='Create new unit test')
    create_test.add_argument("--file_name",
        help='C File name to test'
    )
    build = subparser.add_parser('build', help='Build things')
    build.add_argument('--clean', help='Clean unit test (Ninja)', action='store_true')
    build.add_argument('--clean_all', help='Clean all unit test (CMake+Ninja)', action='store_true')
    build.add_argument('--cmake', help='Run cmake', action='store_true')
    build.add_argument('--run', help='Run unit test (can be filtered)', action='store_true')
    build.add_argument('--filter', help='Filter unit test')
    build.add_argument('--list', help='List unit test (can be filtered)', action='store_true')
    build.add_argument('--ignore_prebuild', help='Will not run prebuild', action='store_true')
    build.add_argument('--ignore_postbuild', help='Will not run postbuild', action='store_true')
    args = parser.parse_args()
    pr = Project(args.project_path)
    if(args.command == "init"):
        process_init(pr, args.name)
    if(args.command == "new"):
        process_new(pr, args)
    if(args.command == "build"):
        process_build(pr, args)
if __name__ == '__main__':
    main()