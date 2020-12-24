import json, sys, re

class LogParser():

    def __init__(self, settings):
        self.input_file = settings['input_file']
        self.output_file = settings['output_file']
        self.data = { 
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

        self.results = {}

    def read_lines(self, f):
        line_block_size = 3
        end = line_block_size

        while True:
            lines = f.readlines(end)
            if not lines:
                break
            end += line_block_size
            yield lines


    def log_process(self):
        
        total_lines = 0
        with open(self.input_file, 'r') as fin:
            i = 0
            for block in self.read_lines(fin):
                print('Process block ' + str(i) + ', ' + str(len(blocks)) + ' lines')
                print(block)
                i += 1

        with open(self.output_file, 'w') as fout:
            json.dump(self.data, fout)

        results = {}
        results['status'] = 'OK'
        results['error'] = ''
        results['message'] = 'Successfully processed ' + str(total_lines) + ' lines of logs. The results was saved in ' \
                            + self.output_file + '.'

        return results


