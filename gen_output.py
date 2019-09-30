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
        print('{s:{c}^{n}}'.format(s=self.name,n=64,c='='))
        for t in self.test:
            print('{:<64} {:>0}'.format(t.test_name, t.result))
        print("="*64)

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
    print('Parsing file: %s'%file_name)

    test_passed = 0
    test_failed = 0
    test_ignored = 0
    ft = FilesTested()
    test_array = []
    print('')
    print('{s:{c}^{n}}'.format(s="Results",n=64,c='='))
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
    print(" Pass : %u"%test_passed)
    print(" Failed : %u"%test_failed)
    print(" Ignored : %u"%test_ignored)
    print('='*64)
                
            #if(r)
process(sys.argv[1])

# check if the output is fixture output (with verbose flag "-v")
    #   if (line.start_with? 'TEST(') || (line.start_with? 'IGNORE_TEST(')
    #     line_array = prepare_fixture_line(line)
    #     if line.include? ' PASS'
    #       test_passed_unity_fixture(line_array)
    #       @test_passed += 1
    #     elsif line.include? 'FAIL'
    #       test_failed_unity_fixture(line_array)
    #       @test_failed += 1
    #     elsif line.include? 'IGNORE'
    #       test_ignored_unity_fixture(line_array)
    #       @test_ignored += 1
    #     end
    #   # normal output / fixture output (without verbose "-v")
    #   elsif line.include? ':PASS'
    #     test_passed(line_array)
    #     @test_passed += 1
    #   elsif line.include? ':FAIL'
    #     test_failed(line_array)
    #     @test_failed += 1
    #   elsif line.include? ':IGNORE:'
    #     test_ignored(line_array)
    #     @test_ignored += 1
    #   elsif line.include? ':IGNORE'
    #     line_array.push('No reason given')
    #     test_ignored(line_array)
    #     @test_ignored += 1
    #   end
    #   @total_tests = @test_passed + @test_failed + @test_ignored
#    File.open(file_name).each do |line|
      # Typical test lines look like these:
      # ----------------------------------------------------
      # 1. normal output:
      # <path>/<test_file>.c:36:test_tc1000_opsys:FAIL: Expected 1 Was 0
      # <path>/<test_file>.c:112:test_tc5004_initCanChannel:IGNORE: Not Yet Implemented
      # <path>/<test_file>.c:115:test_tc5100_initCanVoidPtrs:PASS
      #
      # 2. fixture output
      # <path>/<test_file>.c:63:TEST(<test_group>, <test_function>):FAIL: Expected 0x00001234 Was 0x00005A5A
      # <path>/<test_file>.c:36:TEST(<test_group>, <test_function>):IGNORE
      # Note: "PASS" information won't be generated in this mode
      #
      # 3. fixture output with verbose information ("-v")
      # TEST(<test_group, <test_file>)<path>/<test_file>:168::FAIL: Expected 0x8D Was 0x8C
      # TEST(<test_group>, <test_file>)<path>/<test_file>:22::IGNORE: This Test Was Ignored On Purpose
      # IGNORE_TEST(<test_group, <test_file>)
      # TEST(<test_group, <test_file>) PASS
      #
      # Note: Where path is different on Unix vs Windows devices (Windows leads with a drive letter)!
    #   detect_os_specifics(line)
    #   line_array = line.split(':')

    #   # If we were able to split the line then we can look to see if any of our target words
    #   # were found. Case is important.
    #   next unless (line_array.size >= 4) || (line.start_with? 'TEST(') || (line.start_with? 'IGNORE_TEST(')

    #   # check if the output is fixture output (with verbose flag "-v")
    #   if (line.start_with? 'TEST(') || (line.start_with? 'IGNORE_TEST(')
    #     line_array = prepare_fixture_line(line)
    #     if line.include? ' PASS'
    #       test_passed_unity_fixture(line_array)
    #       @test_passed += 1
    #     elsif line.include? 'FAIL'
    #       test_failed_unity_fixture(line_array)
    #       @test_failed += 1
    #     elsif line.include? 'IGNORE'
    #       test_ignored_unity_fixture(line_array)
    #       @test_ignored += 1
    #     end
    #   # normal output / fixture output (without verbose "-v")
    #   elsif line.include? ':PASS'
    #     test_passed(line_array)
    #     @test_passed += 1
    #   elsif line.include? ':FAIL'
    #     test_failed(line_array)
    #     @test_failed += 1
    #   elsif line.include? ':IGNORE:'
    #     test_ignored(line_array)
    #     @test_ignored += 1
    #   elsif line.include? ':IGNORE'
    #     line_array.push('No reason given')
    #     test_ignored(line_array)
    #     @test_ignored += 1
    #   end
    #   @total_tests = @test_passed + @test_failed + @test_ignored
    # end