import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from symbol import Symbol


class SymbolTest(unittest.TestCase):
    def test_get_price(self):
        symb_vt = Symbol('vt')
        symb_vt._cache_file = os.path.join(os.path.dirname(__file__), 'vt.json')
        self.assertEqual(symb_vt.get_price('2018-06-14'), (76.07, 76.1790, 75.87, 75.97))
        self.assertEqual(symb_vt.get_price('20180614'), (76.07, 76.1790, 75.87, 75.97))
        self.assertIsNone(symb_vt.get_price('20180630'))

        self.assertEqual(symb_vt.get_price(('20180601', '20180615')), (76.26, 76.2800, 75.28, 75.65))
        self.assertEqual(symb_vt.get_price(('20180402', '20180614')), (73.39, 76.2800, 71.60, 75.97))
        self.assertIsNone(symb_vt.get_price(('20180614', '20180630')))


if __name__ == '__main__':
    unittest.main()
