import json, sys, re
'''
class LogParser():

    def __init__(self, file_in, file_out):
        self.fin, self.fout = file_in, file_out
        

    def read_lines(self, lines=128):
        pass
'''


def read_input_file(file_name):
    line_read = 0
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            line_read += 1
            line = f.readline()
    return line_read

def write_output_file():
    dataout = {
        "total_number_of_lines_processed": 4,
        "total_number_of_lines_ok": 4,
        "total_number_of_lines_failed": 0,
        "top_client_ips": {
            "92.177.30.4": 1,
            "51.232.15.21": 1,
            "34.149.47.34": 1,
            "112.21.100.55": 1
        },
        "top_path_avg_seconds": {
            "/admin.php": 0.05,
            "/product/catalog": 1.09,
            "/product/cart": 1.2
        }
    }
    with open('out.json', 'w') as f:
        json.dump(dataout, f)
    return len(json.dumps(dataout))

def process_data():
    print('Log parsing and processing.....')

class LogParser():

    def __init__(self, a, b):
        self.a, self.b = a,b

    def plus_ab(self):
        return self.a + self.b

    def multiply_ab(self):
        return self.a * self.b

def validate_cmd_flags():
    print(sys.argv)

    return True


def log_parser_plugin():

    print('Start Log-Parser......')
    if not validate_cmd_flags():
        print('Invalid command line flags')
        return 1

    lp = LogParser(3,4)
    print("Result from AB:")
    print(lp.plus_ab(), lp.multiply_ab())

    lines = read_input_file('log.txt')
    process_data()
    length = write_output_file()
    print('Read ' + str(lines) + ' lines, write ' + str(length) + ' characters to out.json.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    log_parser_plugin()

