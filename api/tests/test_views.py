from .test_setup import TestSetup

class TestViews(TestSetup):

    def test_get_data(self):
        res = self.client.get(self.test_url)
        self.assertEqual(res.status_code, 200)