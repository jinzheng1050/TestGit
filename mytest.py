
def read_input_file():
    with open('text', 'r') as f:
        line = f.readline()
        while line:
            print(line)
            line = f.readline()

def write_output_file():
    with open('out.txt', 'w') as f:
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
        f.write(dataout)

def process_data():
    print('Log parsing and processing.....')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    print('Start my python')
    read_input_file()
    process_data()
    write_output_file()

