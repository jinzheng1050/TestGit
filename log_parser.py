import json, sys, re, time, traceback
from datetime import datetime

class LogData():

    def __init__(self):
        
        self.beg_time = int(round(time.time()))
        self.end_time = 0
        self.total_read = 0
        self.total_processed = 0
        self.ip_count = {}
        self.path_count = {}

    def __str__(self):
        
        return 'Parsed log data:\n\tRead: ' + str(self.total_read) + ', Processed:' + str(self.total_processed) \
                + ', \n\tTime span: ' + str(self.beg_time) + '-' + str(self.end_time) \
                + ', \n\tIP count: ' + str(self.ip_count) + ', \n\tPath count: ' + str(self.path_count)

    def get_ranked_ips(self, top_n):

        ip_count_ordered = sorted(self.ip_count.items(), key=lambda x:x[1], reverse=True)
        return ip_count_ordered[0:top_n]

    def get_ranked_paths(self, top_n):

        time_span = self.end_time - self.beg_time
        path_avg_seconds = dict([(p, format(float(time_span)/n, '.2f')) for (p, n) in self.path_count.items()])
        path_avg_seconds_ordered = sorted(path_avg_seconds.items(), key=lambda x:x[1])
        return path_avg_seconds_ordered[0:top_n]          


class LogParser():


    def __init__(self, settings):
        self.settings = settings
        self.log_pattern = re.compile(r'((.*) (.*) (.*) (\[(.*)\]) "(.*)" (\d+) (\d+) "(.*)")')    
        self.results = {}


    def _block_read (self, f):

        while True:
            print('Started new block....')
            ln = f.readline()
            if not ln:
                print('finished all blocks')
                break
            lines, count = [ln], 1
            while ln and count < self.settings['line_block_size']:
                ln = f.readline()
                if ln:
                    lines.append(ln)
                    count += 1
            print('to yield...' + str(count) + ' lines')
            print(lines)
            yield lines
 

    def _block_process (self, block, logdata):
        
        logdata.total_read += len(block)
        for log in block:
            try:    
                match = self.log_pattern.match(log)
                if not match: continue
                
                ip = match.group(2)
                logdata.ip_count[ip] = logdata.ip_count.get(ip, 0) + 1
    
                dt = match.group(6)
                dt = datetime.strptime(dt.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                dt_second = int(dt.strftime('%s'))
                logdata.beg_time = min(logdata.beg_time, dt_second)
                logdata.end_time = max(logdata.end_time, dt_second)


                url = match.group(7)
                full_path = url.split(' ')[1]
                path = full_path.split('?')[0]
                logdata.path_count[path] = logdata.path_count.get(path, 0) + 1
                
                logdata.total_processed += 1

            except:
                traceback.print_exc() 
                pass

        print('_block_process done')
        print(logdata)


    def _data_summary (self, logdata):

        data = {}

        data['total_number_of_lines_processed'] = logdata.total_read
        data['total_number_of_lines_ok'] = logdata.total_processed
        data['total_number_of_lines_failed'] = logdata.total_read - logdata.total_processed
        data['top_client_ips'] = logdata.get_ranked_ips(self.settings['max-client-ips'])
        data['top_path_avg_seconds'] = logdata.get_ranked_paths(self.settings['max-path'])
        
        return data


    def log_process (self):
       
        logdata = LogData()
        with open(self.settings['in'], 'r') as fin:
            for block in self._block_read(fin):
                self._block_process(block, logdata)
        
        summary_data = self._data_summary(logdata{}

        with open(self.settings['out'], 'w') as fout:
            json.dump(summary_data, fout)

        print('Final results')
        print(summary_data)

        message = 'Successfully processed ' + str(summary_data['total_number_of_lines_processed']) \
                    + ' lines of logs. The results was saved in ' + self.settings['out'] + '.'
        results = {'status':'OK', 'error':'', 'message':message}

        return results


