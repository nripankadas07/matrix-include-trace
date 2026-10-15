import copy,json,unittest
from pathlib import Path
import matrix_include_trace as m

class Behavior(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((Path(__file__).parent/'example.json').read_text())
    def bad(self):
        with self.assertRaises(m.InputError):m.analyze(self.d)
    def test_unknown_field_rejected(self):
        self.d['unknown']=True;self.bad()

    def test_exclusion_and_independent_append(self):
        r=m.analyze(self.d);self.assertEqual(r['job_count'],4);self.assertEqual(len(r['excluded']),1);self.assertEqual(r['jobs'][-1]['configuration'],{'os':'macos','python':'3.14'})
    def test_added_value_overwrite_allowed(self):
        r=m.analyze(self.d);self.assertFalse(r['jobs'][0]['configuration']['coverage']);self.assertTrue(r['jobs'][2]['configuration']['coverage'])
    def test_appends_never_merge_with_appends(self):
        self.d={'axes':{'os':['linux']},'include':[{'os':'macos'},{'os':'macos','extra':True}]};r=m.analyze(self.d);self.assertEqual(r['job_count'],3);self.assertEqual(r['include_trace'][1]['action'],'append')
    def test_include_only(self):
        self.d={'axes':{},'include':[{'x':1},{'x':2}]};self.assertEqual(m.analyze(self.d)['job_count'],2)
    def test_exclude_before_include_readds(self):
        self.d={'axes':{'x':[1,2]},'exclude':[{'x':2}],'include':[{'x':2}]};r=m.analyze(self.d);self.assertIsNone(r['jobs'][1]['base_index'])
    def test_type_distinct_bool_integer(self):
        self.d={'axes':{'x':[True,1]},'exclude':[{'x':True}]};r=m.analyze(self.d);self.assertEqual(r['job_count'],1);self.assertIs(type(r['jobs'][0]['configuration']['x']),int)
    def test_256_boundary(self):
        self.d={'axes':{'a':list(range(16)),'b':list(range(16))}};self.assertEqual(m.analyze(self.d)['job_count'],256)
    def test_product_limit(self):
        self.d={'axes':{'a':list(range(17)),'b':list(range(16))}};self.bad()
    def test_appended_limit(self):
        self.d={'axes':{'a':list(range(16)),'b':list(range(16))},'include':[{'a':99}]};self.bad()
    def test_duplicate_axis_values(self):
        self.d={'axes':{'x':[1,1]}};self.bad()
    def test_expression_rejected(self):
        self.d={'axes':{'x':['${{ inputs.x }}']}};self.bad()
    def test_object_axis_rejected(self):
        self.d={'axes':{'x':[{'a':1}]}};self.bad()
    def test_unknown_exclude_axis_rejected(self):
        self.d={'axes':{'x':[1]},'exclude':[{'other':2}]};self.bad()
    def test_empty_exclude_rejected(self):
        self.d={'axes':{'x':[1]},'exclude':[{}]};self.bad()
    def test_empty_axis_rejected(self):
        self.d={'axes':{'x':[]}};self.bad()

if __name__ == '__main__':unittest.main()
