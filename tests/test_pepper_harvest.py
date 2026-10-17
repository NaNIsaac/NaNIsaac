import sys
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pepper_harvest import make_svg, demo_contributions, LEVELS

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
    def test_no_empty_calendar_is_accepted(self):
        with self.assertRaises(ValueError):
            make_svg([], theme='light', username='NaNIsaac', assets_dir=ROOT / 'assets' / 'pepper')

if __name__ == '__main__':
    unittest.main()
