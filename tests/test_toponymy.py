from qa.toponymy import get_toponymy, Toponymy


class TestToponymy:

    def test_toponymy(self):
        toponymy = get_toponymy()
        assert type(toponymy) is Toponymy

