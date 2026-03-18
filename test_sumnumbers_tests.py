from unittest import TestCase
from sumnumbers import sum


class Test(TestCase):

    @classmethod
    def setUpClass(self):
        print("Setup Class...")

    @classmethod
    def tearDownClass(self):
        print("Tear Down Class...")

    def setUp(self):
        print("Setup...")

    def tearDown(self):
        print("Tear Down...")

    def test_sum_int_ok(self):
        self.assertEqual(sum(5, 7), 12)

    def test_sum_int_ko(self):
        self.assertNotEqual(sum(5, 7), 15)

    def test_sum_float_ok(self):
        self.assertAlmostEqual(sum(5.2, 7.4), 12.6, 7)

    def test_sum_float_ko(self):
        self.assertNotAlmostEqual(sum(5.2, 7.4), 15.0, 7)

    def test_sum_type_arg1_ko(self):
        self.assertRaises(TypeError, sum, "a", 5)

    def test_sum_type_arg2_ko(self):
        self.assertRaises(TypeError, sum, 5, "b")

    def test_sum_anytype_ok(self):
        param = [(5, 7, 12), (5.2, 7.4, 12.6)]
        for p1, p2, p3 in param:
            with self.subTest():
                self.assertAlmostEqual(sum(p1, p2), p3, 7)
