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
        
        print ('Parsed log data:\n\tRead: ' + str(self.total_read) + ', Processed:' + str(self.total_processed) \
                + ', \n\tTime span: ' + str(self.beg_time) + '-' + str(self.end_time) \
                + ', \n\tIP count: ' + str(self.ip_count) + ', \n\tPath count: ' + str(self.path_count))

    def get_ranked_ips(self, top_n):

        ip_count_ordered = sorted(self.ip_count.items(), key=lambda x:x[1], reverse=True)
        return ip_count_ordered[0:top_n]

    def get_rancked_paths(self, top_n):

        time_span = self.end_time - self.beg_time
        path_avg_seconds = dict([(p, format(float(time_span)/n, '.2f')) for (p, n) in self.path_count.items()])
        path_avg_seconds_ordered = sorted(path_avg_seconds.items(), key=lambda x:x[1])
        return path_avg_seconds_ordered[0:top_n]          


class LogParser():


    def __init__(self, settings):
        self.settings = settings
        self.raw_data = { 
            'beg_time': int(round(time.time())),
            'end_time': 0,
            'total_read': 0,
            'total_processed': 0,
            'ip_count': {},
            'path_count': {},
        }
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
        
        self.raw_data['total_read'] += len(block)
        logdata.total_read += len(block)
        log_pattern = re.compile(r'((.*) (.*) (.*) (\[(.*)\]) "(.*)" (\d+) (\d+) "(.*)")')    
        for log in block:
            try:    
                match = log_pattern.match(log)
                #print('match:')
                #print(match.groups())
                if not match: continue
                
                ip = match.group(2)
                logdata.ip_count[ip] = logdata.ip_count.get(ip, 0) + 1
                #print('ip: ' + ip)
                ip_count_dict = self.raw_data['ip_count']
                ip_count_dict[ip] = ip_count_dict.get(ip,0) + 1
                self.raw_data['ip_count'] = ip_count_dict
                #print(self.raw_data['ip_count'])
                #(self.raw_data['ip_count'])[ip] = (self.raw_data['ip_count'])[ip].get(ip, 0) + 1
    
                dt = match.group(6)
                print(dt + ', ' + ip + ', ' + str(self.raw_data['total_processed']))
                dt = datetime.strptime(dt.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                dt_second = int(dt.strftime('%s'))
                self.raw_data['beg_time'] = min(self.raw_data['beg_time'], dt_second) 
                self.raw_data['end_time'] = max(self.raw_data['end_time'], dt_second) 
                logdata.beg_time = min(logdata.beg_time, dt_second)
                logdata.end_time = max(logdata.end_time, dt_second)


                url = match.group(7)
                full_path = url.split(' ')[1]
                path = full_path.split('?')[0]
                logdata.path_count[path] = logdata.path_count.get(path, 0) + 1
                path_count_dict = self.raw_data['path_count']
                path_count_dict[path] = path_count_dict.get(path, 0) + 1
                self.raw_data['path_count'] = path_count_dict
                #self.raw_data['path_count'][path] = self.raw_data['path_count'][path].get(path, 0) + 1
                
                self.raw_data['total_processed'] += 1
                logdata.total_processed += 1

            except:
                traceback.print_exc() 
                pass

        print('_block_process done')
        print(self.raw_data)
        print(logdata)
        print('raw data above')


    def _data_summary (self):

        data = {}

        data['total_number_of_lines_processed'] = self.raw_data['total_read']
        data['total_number_of_lines_ok'] = self.raw_data['total_processed']
        data['total_number_of_lines_failed'] = data['total_number_of_lines_processed'] \
                                                - data['total_number_of_lines_ok'] 
        ip_count = self.raw_data['ip_count']
        ip_count_ordered = sorted(ip_count.items(), key=lambda x:x[1], reverse=True)
        data['top_client_ips'] = ip_count_ordered[0:self.settings['max-client-ips']]

        time_span = self.raw_data['end_time'] - self.raw_data['beg_time']
        path_count = self.raw_data['path_count']
        path_avg_seconds = dict([(p, format(float(time_span)/n, '.2f')) for (p, n) in path_count.items()])
        path_avg_seconds_ordered = sorted(path_avg_seconds.items(), key=lambda x:x[1])
        data['top_path_avg_seconds'] = path_avg_seconds_ordered[0:self.settings['max-path']]                                        
        return data


    def log_process (self):
       
        logdata = LogData()
        with open(self.settings['in'], 'r') as fin:
            for block in self._block_read(fin):
                self._block_process(block, logdata)
        
        print('before _data_summary()')
        summary = self._data_summary()
        sumdata = {}
        sumdata['total_number_of_lines_processed'] = logdata.total_read
        sumdata['total_number_of_lines_ok'] = logdata.total_processed
        sumdata['total_number_of_lines_failed'] = logdata.total_read - logdata.total_processed
        sumdata['top_client_ips'] = logdata.get_ranked_ips(self.settings['max-client-ips'])
        sumdata['top_path_avg_seconds'] = logdata.get_ranked_paths(self.settings['max-path'])


        with open(self.settings['out'], 'w') as fout:
            json.dump(summary, fout)

        print(summary)
        print(sumdata)

        results = {}
        results['status'] = 'OK'
        results['error'] = ''
        results['message'] = 'Successfully processed ' + str(summary['total_number_of_lines_processed']) \
                            + ' lines of logs. The results was saved in ' + self.settings['out'] + '.'

        return results


