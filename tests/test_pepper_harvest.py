import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pepper_harvest import make_svg, demo_contributions, choose_treats, LEVELS

ROOT = Path(__file__).resolve().parents[1]

class HarvestTests(unittest.TestCase):
    def test_github_levels(self):
        self.assertEqual(len(LEVELS), 5)
        self.assertEqual(LEVELS['NONE'], 0)
    def test_generated_svg_is_valid_and_has_the_right_theme(self):
        weeks = demo_contributions()
        for theme in ('light', 'dark'):
            svg = make_svg(weeks, theme=theme, username='NaNIsaac', assets_dir=ROOT / 'assets' / 'pepper', demo=True)
            ET.fromstring(svg)
            self.assertIn('Pepper\'s Harvest', svg)
            self.assertIn('DEMO / synthetic contributions', svg)
            self.assertIn('repeatCount="indefinite"', svg)
            self.assertIn('data:image/png;base64,', svg)
    def test_treats_are_genuine_contribution_days(self):
        weeks = demo_contributions()
        treats = choose_treats(weeks)
        self.assertGreaterEqual(len(treats), 1)
        self.assertLessEqual(len(treats), 4)
        self.assertEqual(treats, sorted(treats))
        for col, row in treats:
            self.assertGreater(weeks[col][row]["contributionCount"], 0)

    def test_sparse_calendar_does_not_invent_treats(self):
        from copy import deepcopy
        weeks = deepcopy(demo_contributions())
        for w in weeks:
            for d in w:
                d["contributionCount"] = 0
                d["contributionLevel"] = "NONE"
        self.assertEqual(choose_treats(weeks), [])
        svg = make_svg(weeks, theme="dark", username="test", assets_dir=ROOT / 'assets' / 'pepper')
        self.assertIn("sniffs out 0 treats", svg)

    def test_grid_does_not_vanish_and_motions_exist(self):
        weeks = demo_contributions()
        svg = make_svg(weeks, theme='light', username='NaNIsaac', assets_dir=ROOT / 'assets' / 'pepper', demo=True)
        # Old implementation erased each of 53 full columns; new effect targets 4 tiles.
        self.assertEqual(svg.count('stroke="#e8b44b"'), 4)
        self.assertLess(svg.count('<animate attributeName="opacity"'), 40)
        self.assertIn('nom!', svg)
        self.assertIn('rotate(9 32 35)', svg)
        self.assertIn('translate(9 23)', svg)

    def test_no_empty_calendar_is_accepted(self):
        with self.assertRaises(ValueError):
            make_svg([], theme='light', username='NaNIsaac', assets_dir=ROOT / 'assets' / 'pepper')

if __name__ == '__main__':
    unittest.main()
