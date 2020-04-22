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

    def extract_method_from_source(self):
        cmd = """ctags --language-force=C -x --_xformat="%%n:%%N:%%{typeref}:%%{signature}" --kinds-C=f %s"""%self.file_to_parse
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
            if(os.path.isfile(path)):
                return path
        raise Exception("Header to mock not found (%s)"%header_to_mock)

    def create_folder(self):
        print("File", self.file_test)
        shutil.rmtree("mock/%s/"%os.path.basename(self.file_test[:-2]), ignore_errors=True)
        os.makedirs("mock/%s/"%os.path.basename(self.file_test[:-2]))

    def gen_mock_header(self, header_to_mock_path, header_to_mock):
        cfp = CFileParser(header_to_mock_path)
        methods_to_mock = cfp.extract_method()
        output_file_path = "mock/%s/%s"%(os.path.basename(self.file_test[:-2]), "mock_"+header_to_mock)
        output_file_folder = os.path.dirname(output_file_path)
        try:
            os.makedirs(output_file_folder)
        except:
            pass
        with open(output_file_path, "a") as f:
                f.write("#include \"%s\"\n\n"%header_to_mock_path)
        for m in methods_to_mock:
            with open(output_file_path, "a") as f:
                f.write(self.ctags_method_parse_line(m,f)+"\n")


    def ctags_method_parse_one_arg(self, arg):
        if(arg == "void"):
            return [False, ""]
        if(arg == "..."):
            return [False, arg]
        if("[" and "]" in arg):
            index = arg.rfind(" ")
            arg = arg[:index]+" * "+arg[index:]
        if("(*" in arg and arg.count("(") == 2 and arg.count(")") == 2):
            return [True, arg]
        return [False, arg[:arg.rfind(" ")]]

    def ctags_method_parse_sig(self, signature):
        sig = signature[1:-1].split(',')
        sig_parsed = []
        type_def = []
        for s in sig:
            ret = self.ctags_method_parse_one_arg(s)
            if(ret[1] != ""):
                if(ret[0]):
                    sig_parsed.append(ret[1].split("(*")[1].split(")")[0])
                    type_def.append(ret[1])
                else:
                    sig_parsed.append(ret[1])
        return [type_def, sig_parsed]

    def ctags_method_parse_line(self, line, writer):
        if(not len(line)):
            return ""
        ref = line.split(':')
        if(len(ref) != 5):
            return ""
        function_name = ref[1]
        if(ref[2] == "struct"):
            return_ = "struct " + ref[3]
        else:
            return_ = ref[3]
        sign = ref[4]
        parsed_sign = self.ctags_method_parse_sig(sign)
        for t in parsed_sign[0]:
            writer.write("typedef %s;\n"%t)
        func_type = "VALUE"
        start = ""
        if("void" in return_ and not "*" in return_):
            func_type = "VOID"
        else:
            start = return_+", "
        post_type = ""
        if("..." in parsed_sign[1]):
            post_type = "_VARARG"
        FUNC = "FAKE_%s_FUNC%s(%s%s "%(func_type, post_type,start, function_name)
        for sig in parsed_sign[1]:
            FUNC += ", "+sig
        FUNC += ");"
        return FUNC

    def gen_all_mock(self):
        self.create_folder()
        header_to_mock = self.extract_mock_header()
        for h in header_to_mock:
            header_to_mock_path = self.find_header_to_mock(h)
            self.gen_mock_header(header_to_mock_path, h)
            

def main():
    parser = argparse.ArgumentParser("MockGenerator")
    parser.add_argument("--test_file")
    parser.add_argument("--include", nargs='+')
    parser.add_argument("--mock_prefix")
    args = parser.parse_args()
    MockGenerator(args.test_file, args.include, args.mock_prefix)
  

if __name__ == '__main__':
    main()