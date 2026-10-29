"""Behavior tests of citation verification only, not a semantic model evaluation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/insightlens-interview-analysis/scripts/check_evidence.py'
spec = importlib.util.spec_from_file_location('evidence', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
FIXTURE = Path(__file__).parent / 'fixtures/citation-input.json'


class EvidenceChecks(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text())

    def test_exact_membership_and_missing_material(self):
        result = module.check(self.data)
        statuses = {r['id']: r['status'] for r in result['results']}
        self.assertEqual(statuses, dict(E01='match', E02='match', E03='match',
                                       E04='match', E05='mismatch', E06='mismatch',
                                       E07='unverifiable', E08='unverifiable',
                                       E09='unverifiable', E10='mismatch'))

    def test_identical_quotes_in_two_sources_are_both_valid(self):
        result = module.check(self.data)['results']
        self.assertEqual([r['status'] for r in result[2:4]], ['match', 'match'])
        self.assertNotEqual(result[2]['sourceId'], result[3]['sourceId'])

    def test_whitespace_hint_does_not_pass_exact_check(self):
        result = module.check(self.data)['results'][-1]
        self.assertEqual(result['status'], 'mismatch')
        self.assertIn('formattingHint', result)

    def test_duplicate_citation_ids_rejected(self):
        self.data['citations'].append(self.data['citations'][0])
        with self.assertRaises(ValueError):
            module.check(self.data)

    def test_empty_batch_does_not_prove_coverage(self):
        self.data['citations'] = []
        result = module.check(self.data)
        self.assertEqual(result['results'], [])
        self.assertIn('no semantic correctness', result['scope'])

    def test_cli_exit_codes_and_no_input_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            inp = Path(directory) / 'in.json'
            out = Path(directory) / 'out.json'
            inp.write_text(json.dumps(self.data))
            run = subprocess.run([sys.executable, str(SCRIPT), str(inp), '--output', str(out)], capture_output=True)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(out.read_text())['counts']['match'], 4)
            self.data['citations'] = self.data['citations'][:4]
            inp.write_text(json.dumps(self.data))
            self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), str(inp)], capture_output=True).returncode, 0)
            before = inp.read_text()
            self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), str(inp), '--output', str(inp)], capture_output=True).returncode, 2)
            self.assertEqual(inp.read_text(), before)
            inp.write_text('{broken')
            self.assertEqual(subprocess.run([sys.executable, str(SCRIPT), str(inp)], capture_output=True).returncode, 2)


if __name__ == '__main__':
    unittest.main()
