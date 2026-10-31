import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import paradox
from audit_linux_paths import audit
from compare_runtime_logs import compare

class ToolsTest(unittest.TestCase):
    def test_lossless_edit_ignores_comment_braces(self):
        source='# { comment\nitem = { label = "quoted } brace" count = 4 }\n'
        entry=paradox.fields(paradox.parse(source)[0],'count')[0]
        changed=paradox.apply(source,[(entry.value_start,entry.value_end,'7')])
        self.assertEqual(changed,source.replace('count = 4','count = 7'))
    def test_unclosed_block_rejected(self):
        with self.assertRaises(ValueError): paradox.parse('item = { count = 4')
    def test_case_mismatch_and_unresolved_are_distinct(self):
        with tempfile.TemporaryDirectory() as tmp:
            game=Path(tmp)/'game';mod=Path(tmp)/'mod';game.mkdir();mod.mkdir()
            (game/'gfx').mkdir();(game/'gfx'/'Icon.dds').write_bytes(b'')
            (mod/'refs.txt').write_text('icon = "gfx/icon.dds" missing = "gfx/missing.dds"')
            report=audit(game,mod)
            self.assertEqual(len(report['case_mismatches']),1)
            self.assertEqual(len(report['unresolved_or_dlc_paths']),1)
            self.assertFalse(report['linux_runtime_verified'])
    def test_shared_fingerprint_ignores_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            baseline=Path(tmp)/'base';core=Path(tmp)/'core'
            baseline.write_text('[00:01][E][example.cpp:1]: Error one\n')
            core.write_text('[00:02][E][example.cpp:1]: Error one\n[00:03][E][example.cpp:2]: Error two\n')
            report=compare(baseline,core)
            self.assertEqual(report['shared_unique'],1)
            self.assertEqual(len(report['core_unmatched']),1)

if __name__=='__main__': unittest.main()
