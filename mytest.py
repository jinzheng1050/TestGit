def read_input_file():
    with open('text', 'r') as f:
        line = f.readline()
        while line:
            print(line)
            line = f.readline()

def write_output_file():
    print('To be done')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Start my python')
    read_input_file()
    write_output_file()

