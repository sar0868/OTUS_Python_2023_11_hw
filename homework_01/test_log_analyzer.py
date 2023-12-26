import itertools
import unittest

import log_analyzer


class TestLogAnalyzer(unittest.TestCase):

    def setUp(self):
        self.data = [
            b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390',
            b'1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" 0.133',
            b'1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" 0.199',
            b'1.199.4.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/slot/4705/groups HTTP/1.1" 200 2613 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-3800516057-4708-9752745" "2a828197ae235b0b3cb" 0.704',
            b'1.168.65.96 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/internal/banner/24294027/info HTTP/1.1" 200 407 "-" "-" "-" "1498697422-2539198130-4709-9928846" "89f7f1be37d" 0.146',
            b'1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 1020 "-" "Configovod" "-" "1498697422-2118016444-4708-9752747" "712e90144abee9" 0.628',
            b'1.194.135.240 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/group/7786679/statistic/sites/?date_type=day&date_from=2017-06-28&date_to=2017-06-28 HTTP/1.1" 200 22 "-" "python-requests/2.13.0" "-" "1498697422-3979856266-4708-9752772" "8a7741a54297568b" 0.067',
            b'1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "POST /api/v2/banner/1717161 HTTP/1.1" 200 2116 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752771" "712e90144abee9" 0.138',
            b'1.166.85.48 -  - [29/Jun/2017:03:50:22 +0300] "GET /export/appinstall_raw/2017-06-29/ HTTP/1.0" 200 28358 "-" "Mozilla/5.0 (Windows; U; Windows NT 6.0; ru; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)" "-" "-" "-" 0.003',
            b'1.199.4.96 -  - [29/Jun/2017:03:50:22 +0300] "POST /api/v2/slot/4822/groups HTTP/1.1" 200 22 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-3800516057-4708-9752773" "2a828197ae235b0b3cb" 0.157',
            b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "PUT /api/v2/banner/25019354 HTTP/1.1" 200 883 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752753" "dc7161be3" 0.726',
        ]
        self.data_error = [
            b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390',
            b'1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "GET /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" error',
            b'1.199.4.96 -  - [29/Jun/2017:03:50:22 +0300] "POST /api/v2/slot/4822/groups HTTP/1.1" 200 22 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-3800516057-4708-9752773" "2a828197ae235b0b3cb" 0.157',
            b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "PUT /api/v2/banner/25019354 HTTP/1.1" 200 883 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752753" "dc7161be3" 0.726',
        ]

    def tearDown(self):
        pass

    def test_parse_data(self):
        result_list = list(log_analyzer.gen_grep(self.data))
        self.assertEqual(len(result_list), 8)

    def test_gen_grep(self):
        data = [
            b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390',
            b'1.99.174.176 3b81f63526fa8  - [29/Jun/2017:03:50:22 +0300] "POST /api/1/photogenic_banners/list/?server_name=WIN7RB4 HTTP/1.1" 200 12 "-" "Python-urllib/2.7" "-" "1498697422-32900793-4708-9752770" "-" 0.133', ]

        result = list(log_analyzer.gen_grep(data))
        self.assertEqual(len(result), 1)

    def test_parse_line(self):
        pipline = log_analyzer.gen_grep(self.data)
        result = list(log_analyzer.parse_line(pipline))
        pattern = [
            "0.390", "0.133", "0.199", "0.704", "0.146", "0.628", "0.067", "0.003"
        ]
        total_time = list(itertools.accumulate([float(i) for i in pattern]))[-1]
        print(total_time)
        self.assertEqual([el[-1] for el in result], pattern)


    def test_calculation_report(self):
        pathlines = log_analyzer.gen_grep(self.data)
        records = log_analyzer.parse_line(pathlines)
        calculation = log_analyzer.calculation_report(records, 0.001)
        result = calculation['/api/v2/banner/25019354']
        self.assertEqual(result.url, '/api/v2/banner/25019354')
        self.assertEqual(result.count, 3)
        self.assertTrue(abs(result.count_perc - 37.5) < 0.001)
        self.assertTrue(abs(result.time_sum - 1.217) < 0.00001)
        self.assertTrue(abs(result.time_perc - 53.61233) < 0.00001)
        self.assertTrue(abs(result.time_avg - 0.40566) < 0.00001)
        self.assertEqual(result.time_max, 0.628)
        self.assertTrue(abs(result.time_med - 0.39) < 0.00001)

    def test_calculation_report_error(self):
        pathlines = log_analyzer.gen_grep(self.data_error)
        records = log_analyzer.parse_line(pathlines)
        calculation = log_analyzer.calculation_report(records, 51.0)
        print(calculation)
        result = calculation['/api/v2/banner/25019354']

        self.assertEqual(result.url, '/api/v2/banner/25019354')
        self.assertEqual(result.count, 1)
        self.assertTrue(abs(result.count_perc - 100) < 0.001)
        self.assertTrue(abs(result.time_sum - 0.39) < 0.00001)
        self.assertTrue(abs(result.time_perc - 100) < 0.00001)
        self.assertTrue(abs(result.time_avg - 0.39) < 0.00001)
        self.assertEqual(result.time_max, 0.39)
        self.assertTrue(abs(result.time_med - 0.39) < 0.00001)


if __name__ == '__main__':
    unittest.main()
