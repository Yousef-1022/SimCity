import unittest
from models.Citizen import Citizen
from models.Utils import *

class TestCitizen(unittest.TestCase):

    def test_citizen_creation(self):
        # add 10 citizens
        Citizen.citizens = {}
        initial_citizens = []
        for i in range (1,11):
            c = Citizen()
            initial_citizens.append(c)

        assert 10 == len(initial_citizens)

        for i in range (11,21):
            c = Citizen()
            initial_citizens.append(c)

        assert 20 == len(initial_citizens)

    def test_delete_citizens(self):
        # add 10 citizens
        Citizen.citizens = {}
        citizens = []
        for i in range (1,11):
            c = Citizen()
            citizens.append(c)

        assert 10 == len(citizens)

        # delete one citizen
        assert True == delete_citizen(citizens[0])

        # check if deleted
        assert 9 == len(Citizen.get_all_citizens())

    def test_get_all_citizens(self):
        Citizen.citizens = {}
        # create initial citizens
        citizens = []
        for i in range(1,11):
            c = Citizen()
            citizens.append(c)
        assert 10 == len(Citizen.get_all_citizens())

        # test for more than 100 citizen
        # create 100 citizens more
        for i in range(11,111):
            c = Citizen()
            citizens.append(c)
        assert 110 == len(Citizen.get_all_citizens())

        # test after deleting citizens
        for i in range(0,100):
            delete_citizen(citizens[i])
        assert 10 == len(Citizen.get_all_citizens())

    def test_get__citizens_len(self):
        Citizen.citizens = {}
        # create initial citizens
        citizens = []
        for i in range(1,11):
            c = Citizen()
            citizens.append(c)
        assert 10 == c.get_citizens_len()

        # test for more than 100 citizen
        # create 100 citizens more
        for i in range(11,111):
            c = Citizen()
            citizens.append(c)
        assert 110 == c.get_citizens_len()

        # test after deleting citizens
        for i in range(0,100):
            delete_citizen(citizens[i])
        assert 10 == c.get_citizens_len()


if __name__ == '__main__':
    unittest.main()
