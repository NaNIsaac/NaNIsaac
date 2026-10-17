import re
import sys
import unittest
import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pepper_harvest import (FRAMES, LEVELS, PRINT_LIFE, Timeline, choose_treats,
                            demo_contributions, make_svg)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'pepper'


def render(weeks, theme='light', demo=True):
    return make_svg(weeks, theme=theme, username='NaNIsaac', assets_dir=ASSETS, demo=demo)


def visible_at(svg, t):
    """Frame names whose discrete opacity animation is 1 at time t."""
    dur = float(re.search(r'dur="([\d.]+)s"', svg).group(1))
    pepper = svg[svg.index('<g id="pepper">'):]
    shown = []
    for name, values, keys in zip(FRAMES, *zip(*re.findall(
            r'<image [^>]*><animate attributeName="opacity" values="([^"]*)" keyTimes="([^"]*)"', pepper))):
        state = '0'
        for v, k in zip(values.split(';'), keys.split(';')):
            if float(k) * dur <= t:
                state = v
        if state == '1':
            shown.append(name)
    return shown


class HarvestTests(unittest.TestCase):
    def test_github_levels(self):
        self.assertEqual(len(LEVELS), 5)
        self.assertEqual(LEVELS['NONE'], 0)

    def test_every_frame_exists_on_one_canvas(self):
        sizes = set()
        for name in FRAMES:
            data = (ASSETS / 'frames' / f'{name}.png').read_bytes()
            sizes.add((int.from_bytes(data[16:20], 'big'), int.from_bytes(data[20:24], 'big')))
        self.assertEqual(sizes, {(86, 68)})

    def test_generated_svg_is_valid_for_both_themes(self):
        weeks = demo_contributions()
        for theme in ('light', 'dark'):
            svg = render(weeks, theme)
            ET.fromstring(svg)
            self.assertIn("Pepper's Harvest", svg)
            self.assertIn('DEMO / synthetic contributions', svg)
            self.assertNotIn('<script', svg)

    def test_loop_is_about_26_seconds(self):
        svg = render(demo_contributions())
        dur = float(re.search(r'dur="([\d.]+)s"', svg).group(1))
        self.assertTrue(22 <= dur <= 30, dur)

    def test_exactly_one_frame_is_visible_at_any_time(self):
        svg = render(demo_contributions())
        dur = float(re.search(r'dur="([\d.]+)s"', svg).group(1))
        t = 0.013
        while t < dur:
            self.assertEqual(len(visible_at(svg, t)), 1, t)
            t += 0.071

    def test_poses_are_distinct_and_end_seated(self):
        svg = render(demo_contributions())
        dur = float(re.search(r'dur="([\d.]+)s"', svg).group(1))
        seen = {visible_at(svg, t / 10)[0][:-1] for t in range(int(dur * 10))}
        self.assertEqual(seen, {'walk', 'sniff', 'dig', 'eat', 'sit'})
        self.assertEqual(visible_at(svg, dur - 0.05)[0][:-1], 'sit')

    def test_treats_are_genuine_contribution_days(self):
        weeks = demo_contributions()
        treats = choose_treats(weeks)
        self.assertTrue(1 <= len(treats) <= 3)
        self.assertEqual(treats, sorted(treats))
        for col, row in treats:
            self.assertGreater(weeks[col][row]['contributionCount'], 0)

    def test_sparse_calendar_does_not_invent_treats(self):
        weeks = deepcopy(demo_contributions())
        for w in weeks:
            for d in w:
                d['contributionCount'] = 0
                d['contributionLevel'] = 'NONE'
        self.assertEqual(choose_treats(weeks), [])
        svg = render(weeks, 'dark', demo=False)
        self.assertIn('sniffs out 0 treats', svg)
        self.assertNotIn('class="event"', svg)

    def test_only_event_tiles_react(self):
        svg = render(demo_contributions())
        self.assertEqual(svg.count('class="event"'), len(choose_treats(demo_contributions())))

    def test_paw_prints_follow_steps_and_stay_few(self):
        tl = Timeline(0, 50)
        tl.walk(300, 50)
        times = [c[0] for c in tl.contacts]
        sides = [c[3] for c in tl.contacts]
        self.assertTrue(all(a != b for a, b in zip(sides, sides[1:])))  # left, right, left...
        gaps = [b - a for a, b in zip(times, times[1:])]
        alive = PRINT_LIFE / (sum(gaps) / len(gaps))
        self.assertTrue(3 <= alive <= 6.5, alive)
        xs = [c[1] for c in tl.contacts]
        self.assertEqual(xs, sorted(xs))

    def test_no_empty_calendar_is_accepted(self):
        with self.assertRaises(ValueError):
            make_svg([], theme='light', username='NaNIsaac', assets_dir=ASSETS)


if __name__ == '__main__':
    unittest.main()
