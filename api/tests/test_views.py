from .test_setup import TestSetup
import pdb

class TestViews(TestSetup):

    def test_get_data(self):
        res = self.client.get(self.test_url)
        pdb.set_trace()
        self.assertEqual(res.status_code, 200)