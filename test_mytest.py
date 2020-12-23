import mytest

class TestMytest:

    def test_read_input_file(self):
        assert 5 == mytest.read_input_file()

    def test_write_output_file(self):
        assert 293 == mytest.write_output_file()
