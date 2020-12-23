import mytest

class TestMytest:

    def test_read_input_file(self):
        assert 4 == mytest.read_input_file('log.txt')

    def test_write_output_file(self):
        assert 294 == mytest.write_output_file()
