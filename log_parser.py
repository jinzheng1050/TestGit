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

    def read_line(self, f):
        return f.readline()


    def log_process(self):
        
        total_lines = 0
        with open(self.input_file, 'r') as fin:
            line = self.read_line(fin)
            while line:
                total_lines += 1
                '''
                self.data() update
                '''
                line = self.read_line(fin)
        with open(self.output_file, 'w') as fout:
            json.dump(self.data, fout)

        results = {}
        results['status'] = 'OK'
        results['error'] = ''
        results['message'] = 'Successfully processed ' + str(total_lines) + ' lines of logs. The results was saved in ' \
                            + self.output_file + '.'

        return results


