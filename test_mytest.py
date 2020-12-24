import mytest

class TestMytest:

    def test_read_input_file(self):
        assert 4 == mytest.read_input_file('log.txt')

    def test_write_output_file(self):
        assert 294 == mytest.write_output_file()

    def test_plus_ab(self):
        lp = LogParser()
        assert 7 == lp.plus_ab(3,4)

    def test_multiply_ab(self):
        jp = LogParser()
        assert 18 == lp.multiply(3,6)
