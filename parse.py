import subprocess
import os
from subprocess import check_output
import shlex
import shutil
import argparse

class CFileParser():
    def __init__(self, file_to_parse):
        self.file_to_parse = file_to_parse

    def extract_included_header(self):
        cmd = """ctags -x --_xformat="%%N" -o - --extras=r --kinds-C=h --language-force=C %s"""%self.file_to_parse
        output = check_output(shlex.split(cmd))
        headers = output.splitlines()
        included_headers = []
        for h in headers:
            included_headers.append(h)
        return included_headers

    def extract_method(self):
        cmd = """ctags --language-force=C -x --_xformat="%%n:%%N:%%{typeref}:%%{signature}" --kinds-C=p %s"""%self.file_to_parse
        methods_string = check_output(shlex.split(cmd))
        methods_list = methods_string.splitlines()
        parsed_methods_list = []         
        for m in methods_list:
            if(len(m)):
                parsed_methods_list.append(m)
        return parsed_methods_list

class MockGenerator():
    def __init__(self, file_test, include_list, mock_prefix):
        self.file_test = file_test
        self.include_list = include_list
        self.mock_prefix = mock_prefix
        self.gen_all_mock()

    def extract_mock_header(self):
        cfp = CFileParser(self.file_test)
        mock_header_list = []
        for m in cfp.extract_included_header(): 
            if(m.startswith(self.mock_prefix)):
                mock_header_list.append(m[len(self.mock_prefix):])
        return mock_header_list
    
    def find_header_to_mock(self, header_to_mock):
        for i in self.include_list:
            path = os.path.join(os.path.realpath(i), header_to_mock)
            print path
            if(os.path.isfile(path)):
                return path
        raise Exception("Header to mock not found")

    def create_folder(self):
        shutil.rmtree("build/mock/%s/"%os.path.basename(self.file_test[:-2]), ignore_errors=True)
        os.makedirs("build/mock/%s/"%os.path.basename(self.file_test[:-2]))

    def gen_mock_header(self, header_to_mock_path):
        cfp = CFileParser(header_to_mock_path)
        methods_to_mock = cfp.extract_method()
        for m in methods_to_mock:
            with open("build/mock/%s/%s"%(os.path.basename(self.file_test[:-2]), "mock_"+os.path.basename(header_to_mock_path)), "a") as f:
                f.write(self.ctags_method_parse_line(m)+"\n")


    def ctags_method_parse_one_arg(self, arg):
        if(arg == "void"):
            return ""
        if(arg == "..."):
            return arg
        if("[" and "]" in arg):
            index = arg.rfind(" ")
            arg = arg[:index]+" * "+arg[index:]
        return arg[:arg.rfind(" ")]

    def ctags_method_parse_sig(self, signature):
        sig = signature[1:-1].split(',')
        sig_parsed = []
        for s in sig:
            ret = self.ctags_method_parse_one_arg(s)
            if(ret != ""):
                sig_parsed.append(self.ctags_method_parse_one_arg(s))
        return sig_parsed

    def ctags_method_parse_line(self, line):
        if(not len(line)):
            return
        ref = line.split(':')
        function_name = ref[1]
        return_ = ref[3]
        sign = ref[4]
        parsed_sign = self.ctags_method_parse_sig(sign)
        func_type = "VALUE"
        start = ""
        if(return_ == "void"):
            func_type = "VOID"
        else:
            start = return_+", "
        post_type = ""
        print "PARSE_SIGN : ", parsed_sign
        if("..." in parsed_sign):
            post_type = "_VARARG"
        FUNC = "FAKE_%s_FUNC%s(%s%s "%(func_type, post_type,start, function_name)
        for sig in parsed_sign:
            FUNC += ", "+sig
        FUNC += ");"
        return FUNC

    def gen_all_mock(self):
        self.create_folder()
        header_to_mock = self.extract_mock_header()
        for h in header_to_mock:
            print "Mocking %s"%h
            header_to_mock_path = self.find_header_to_mock(h)
            self.gen_mock_header(header_to_mock_path)
            

def main():
    parser = argparse.ArgumentParser("MockGenerator")
    parser.add_argument("--test_file")
    parser.add_argument("--include", nargs='+')
    parser.add_argument("--mock_prefix")
    args = parser.parse_args()
    print args.include
    MockGenerator(args.test_file, args.include, args.mock_prefix)
    #mg = MockGenerator("test/test_abl_sensorsync_mqtt_process.c", ["../Libraries/ABL_Sensor_Sync/Streaming/", "../SDK/esp-idf/components/log/include/"], "mock_")


if __name__ == '__main__':
    main()