import unittest
from main import calcul_group_user


class TestCalculGroupUser(unittest.TestCase):
    def test_calcul_group_user(self):
        actual = calcul_group_user(5, 21, False)
        expected = "Nombre de groupes maximum = 5 | Nombre de personnes par groupes simples = 4 | Nombre de personnes dans le dernier groupe = 5"
        self.assertEqual(actual, expected)
