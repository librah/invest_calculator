import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import symbol

symbol.cache_dir = os.path.dirname(__file__)


class SymbolTest(unittest.TestCase):
    def test_get_price_alphavantage_json(self):
        symb_vt = symbol.Symbol('vt')
        self.assertEqual(symb_vt.get_price('2018-06-14'), (76.07, 76.1790, 75.87, 75.97))
        self.assertEqual(symb_vt.get_price('20180614'), (76.07, 76.1790, 75.87, 75.97))
        self.assertIsNone(symb_vt.get_price('20180630'))

        self.assertEqual(symb_vt.get_price(('20180601', '20180615')), (76.26, 76.2800, 75.28, 75.65))
        self.assertEqual(symb_vt.get_price(('20180402', '20180614')), (73.39, 76.2800, 71.60, 75.97))
        self.assertIsNone(symb_vt.get_price(('20180614', '20180630')))

    def test_get_price_cnyes_csv(self):
        symb_50 = symbol.Symbol('0050')
        self.assertEqual(symb_50.get_price('20160726'), (69.0, 69.4, 68.85, 69.4))
        self.assertEqual(symb_50.get_price('20180615'), (81.60, 81.95, 81.20, 81.95))
        self.assertEqual(symb_50.get_price(('20160726', '20160801')), (69.0, 69.95, 68.85, 69.7))
        self.assertEqual(symb_50.get_price(('20160726', '20180614')), (69.00, 83.10, 68.85, 81.75))

if __name__ == '__main__':
    unittest.main()
