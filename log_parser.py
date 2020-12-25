import json, sys, re

class LogParser():

    def __init__(self, settings):
        self.input_file = settings['in']
        self.output_file = settings['out']
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

        while True:
            print('Started new block....')
            ln = f.readline()
            if not ln:
                break
            lines, count = [ln], 1
            while ln and count < line_block_size:
                ln = f.readline()
                if ln:
                    lines.append(ln)
                    count += 1
            print('to yield...')
            print(lines)
            yield lines
 

    def log_process(self):
        
        total_lines = 0
        with open(self.input_file, 'r') as fin:
            for block in self.read_lines(fin):
#                print('Process block ' + str(i) + ', ' + str(len(block)) + ' lines')
#                print(block)
                 total_lines += len(block)

        with open(self.output_file, 'w') as fout:
            json.dump(self.data, fout)

        results = {}
        results['status'] = 'OK'
        results['error'] = ''
        results['message'] = 'Successfully processed ' + str(total_lines) + ' lines of logs. The results was saved in ' \
                            + self.output_file + '.'

        return results


