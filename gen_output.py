import sys
import os

class Test:
    def __init__(self, line_array):
        self.line_array = line_array
        self.file_name = os.path.splitext(os.path.basename(line_array[0]))[0]
        self.test_name = '_'.join(line_array[2].split("_")[1:])
        if(len(line_array) > 4):
            self.result = "%s \n\t(%s)"%(line_array[3], ':'.join(line_array[4:]).strip())
        else:
            self.result = line_array[3].strip()
        
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

    def add_file_tested(self, file_name):
        already_there = False
        for f in self.file_tested:
            if(f.name == file_name):
                already_there = True
                break
        if(not already_there):
            self.file_tested.append(FileTested(file_name))

    def add_test_to_file(self, test):
        test = Test(test)
        for f in self.file_tested:
            if(test.file_name == f.name):
                f.add_test(test)

    def print_summary(self):
        for f in self.file_tested:
            f.print_summary()

def process(file_name):
    test_passed = 0
    test_failed = 0
    test_ignored = 0
    ft = FilesTested()
    test_array = []
    print('')
    print('{s:{c}^{n}}'.format(s=" Results ",n=72,c='='))
    print('')
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for r in lines:
            line_array = r.split(":")
            if(((len(line_array) >= 4) or r.startswith('TEST(') or r.startswith('IGNORE_TEST(')) and not ("time elapsed" in r)):
                file_name = os.path.splitext(os.path.basename(line_array[0]))[0]
                ft.add_file_tested(file_name)
                if("PASS" in r):
                    test_passed +=1
                    ft.add_test_to_file(line_array)
                if("FAIL" in r):
                    test_failed +=1
                    ft.add_test_to_file(line_array)
                if("IGNORE" in r):
                    test_failed +=1
                    ft.add_test_to_file(line_array)
    ft.print_summary()
    print("Pass : %u"%test_passed)
    print("Failed : %u"%test_failed)
    print("Ignored : %u"%test_ignored)
    print('='*72)

process(sys.argv[1])
