import sys
import os

class Test:
    def __init__(self, line_array):
        self.line_array = line_array
        self.file_name = os.path.splitext(os.path.basename(line_array[0]))[0]
        self.test_name = '_'.join(line_array[2].split("_")[1:])
        self.status = line_array[3].strip()
        if(len(line_array) > 4):
            self.result = "%s \n\t(%s)"%(self.status, ':'.join(line_array[4:]).strip())
        else:
            self.result = self.status
        
class FileTested:
    def __init__(self, name):
        self.name = name
        self.test = []

    def add_test(self, val):
        self.test.append(val)

    def print_summary(self):
        print('{s:{c}^{n}}'.format(s=" "+self.name+" ",n=72,c='='))
        for t in self.test:
            print('{:<64} {:>0}'.format(t.test_name, t.result))
        print("="*72)

class FilesTested:
    def __init__(self):
        self.file_tested = []
        self.test_passed = 0
        self.test_ignored = 0
        self.test_failed = 0
        self.test_number = 0

    def add_file_tested(self, file_name):
        already_there = False
        for f in self.file_tested:
            if(f.name == file_name):
                already_there = True
                break
        if(not already_there):
            self.file_tested.append(FileTested(file_name))

    def add_test_to_file(self, test_line_array):
        test = Test(test_line_array)
        for f in self.file_tested:
            if(test.file_name == f.name):
                line = ':'.join(test_line_array)
                if("PASS" in line):
                    self.test_passed +=1
                if("FAIL" in line):
                    self.test_failed +=1
                if("IGNORE" in line):
                    self.test_ignored +=1
                self.test_number += 1
                f.add_test(test)

    def print_summary(self):
        for f in self.file_tested:
            f.print_summary()
        print("Pass : %u"%self.test_passed)
        print("Failed : %u"%self.test_failed)
        print("Ignored : %u"%self.test_ignored)
        print('='*72)

class OutputGenerator:
    def __init__(self, file_name):
        self.file_name = file_name
        self.ft = FilesTested()

    def process_file(self):
        print('')
        print('{s:{c}^{n}}'.format(s=" Results ",n=72,c='='))
        print('')
        with open(self.file_name, 'r') as f:
            lines = f.readlines()
            for r in lines:
                line_array = r.split(":")
                if(((len(line_array) >= 4) or r.startswith('TEST(') or r.startswith('IGNORE_TEST(')) and not ("time elapsed" in r)):
                    self.file_name = os.path.splitext(os.path.basename(line_array[0]))[0]
                    self.ft.add_file_tested(self.file_name)
                    self.ft.add_test_to_file(line_array)
        self.ft.print_summary()

    def gen_xml(self):
        with open("report.xml", 'w') as f:
            f.write("<?xml version='1.0' encoding='utf-8' ?>\n")
            f.write("<TestRun>\n")
            if(not self.ft.test_ignored):
                f.write("\t<IgnoredTests/>\n")
            else:
                f.write("\t<IgnoredTests>\n")
                i = 1
                for ftested in self.ft.file_tested:
                    for t in ftested.test:
                        if t.status == "IGNORE":
                            f.write("""\t\t<Test id="%u">\n"""%i)
                            f.write("\t\t\t<Name>%s::%s</Name>\n"%(t.line_array[0],t.test_name))
                            f.write("\t\t</Test>\n")
                            i+=1
                f.write("\t</IgnoredTests>\n")
            if(not self.ft.test_failed):
                f.write("\t<FailedTests/>\n")
            else:
                f.write("\t<FailedTests>\n")
                i = 1
                for ftested in self.ft.file_tested:
                    for t in ftested.test:
                        if t.status == "FAIL":
                            f.write("""\t\t<Test id="%u">\n"""%i)
                            f.write("\t\t\t<Name>%s::%s</Name>\n"%(t.line_array[0],t.test_name))
                            f.write("\t\t</Test>\n")
                            i+=1
                f.write("\t</FailedTests>\n")
            if(not self.ft.test_passed):
                f.write("\t<SuccessfulTests/>\n")
            else:
                f.write("\t<SuccessfulTests>\n")
                i = 1
                for ftested in self.ft.file_tested:
                    for t in ftested.test:
                        if t.status == "PASS":
                            f.write("""\t\t<Test id="%u">\n"""%i)
                            f.write("\t\t\t<Name>%s::%s</Name>\n"%(t.line_array[0],t.test_name))
                            f.write("\t\t</Test>\n")
                            i+=1
                f.write("\t</SuccessfulTests>\n")
            f.write("\t<Statistics>\n")
            f.write("\t\t<Tests>%u</Tests>\n"%(self.ft.test_number))
            f.write("\t\t<Ignores>%u</Ignores>\n"%(self.ft.test_ignored))
            f.write("\t\t<FailuresTotal>%u</FailuresTotal>\n"%(0))
            f.write("\t\t<Failures>%u</Failures>\n"%(self.ft.test_failed))
            f.write("\t\t<Errors>%u</Errors>\n"%(0))
            f.write("\t</Statistics>\n")
            f.write("</TestRun>\n")


g = OutputGenerator(sys.argv[1])
g.process_file()
g.gen_xml()