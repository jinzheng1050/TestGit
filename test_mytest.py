import mytest
from log_parser import LogParser


class TestMytest:

    def test_read_input_file(self):
        assert 4 == mytest.read_input_file('log.txt')

    def test_write_output_file(self):
        assert 294 == mytest.write_output_file()

    def test_plus_ab(self):
        lp = LogParser(3,4)
        assert 7 == lp.plus_ab()

    def test_multiply_ab(self):
        lp = LogParser(3,6)
        assert 18 == lp.multiply_ab()
