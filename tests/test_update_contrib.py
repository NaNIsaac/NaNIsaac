import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from update_contrib import LIMIT, fill, research_block, upstream_block

ROOT = Path(__file__).resolve().parents[1]


def pr(repo, number, merged=False, open_=False):
    return {
        'repository_url': f'https://api.github.com/repos/{repo}',
        'html_url': f'https://github.com/{repo}/pull/{number}',
        'title': f'change {number}',
        'state': 'open' if open_ else 'closed',
        'pull_request': {'merged_at': '2026-10-17T11:39:08Z' if merged else None},
    }


class ResearchBlock(unittest.TestCase):
    def test_heading_and_merged_before_open(self):
        block = research_block([
            pr('NaNIsaac-Research/TraTT', 3, open_=True),
            pr('NaNIsaac-Research/TraTT', 2, merged=True),
            pr('NaNIsaac-Research/TraTT', 1),
        ])
        lines = block.splitlines()
        self.assertEqual(lines[0], '### Research organization')
        self.assertNotIn('Upstream', block)
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[2].endswith('<sub>merged</sub>') and lines[3].endswith('<sub>open</sub>'))
        self.assertNotIn('/pull/1)', block, 'closed without merge is not listed')

    def test_limit(self):
        prs = [pr('NaNIsaac-Research/TraTT', n, merged=True) for n in range(LIMIT + 3)]
        self.assertEqual(research_block(prs).count('\n- '), LIMIT)


class UpstreamBlock(unittest.TestCase):
    def test_no_section_without_a_third_party_merge(self):
        self.assertEqual(upstream_block([]), '')
        self.assertEqual(upstream_block([
            pr('tomopy/tomopy', 9, open_=True),
            pr('python/cpython', 8),
            pr('Q07K/prompt-gallery', 7, merged=True),
            pr('center4upt/XFEL_data', 6, merged=True),
        ]), '')

    def test_merged_third_party_pull_requests_only(self):
        block = upstream_block([
            pr('dkriegner/xrayutilities', 5, open_=True),
            pr('pydata/xarray', 4, merged=True),
            pr('Q07K/prompt-gallery', 3, merged=True),
        ])
        self.assertTrue(block.startswith('### Upstream\n\n'))
        self.assertIn('pydata/xarray/pull/4', block)
        self.assertNotIn('xrayutilities', block)
        self.assertNotIn('prompt-gallery', block)


class Fill(unittest.TestCase):
    def test_empty_block_removes_the_section_and_keeps_the_markers(self):
        text = 'a\n<!-- upstream:start -->\n### Upstream\n\n- old\n<!-- upstream:end -->\nb'
        self.assertEqual(fill(text, 'upstream', ''), 'a\n<!-- upstream:start -->\n<!-- upstream:end -->\nb')
        again = fill(fill(text, 'upstream', ''), 'upstream', '### Upstream\n\n- new')
        self.assertIn('### Upstream\n\n- new\n<!-- upstream:end -->', again)

    def test_readme_has_both_marker_pairs(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for name in ('research', 'upstream'):
            self.assertEqual(readme.count(f'<!-- {name}:start -->'), 1)
            self.assertEqual(readme.count(f'<!-- {name}:end -->'), 1)
        self.assertNotIn('contrib:start', readme)


if __name__ == '__main__':
    unittest.main()
