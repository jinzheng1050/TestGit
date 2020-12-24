import json, sys, re
from log_parser import LogParser

def read_input_file(file_name):
    line_read = 0
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            line_read += 1
            line = f.readline()
    return line_read


def write_output_file(file_name):
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
    with open(file_name, 'w') as f:
        json.dump(dataout, f)
    return len(json.dumps(dataout))


def process_data():
    print('Log parsing and processing.....')


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
    length = write_output_file('results.json')
    print('Read ' + str(lines) + ' lines, write ' + str(length) + ' characters to out.json.')


if __name__ == '__main__':

    log_parser_plugin()



