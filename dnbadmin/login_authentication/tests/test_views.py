''' Test Views '''
from .test_setup import TestSetUp


class TestViews(TestSetUp):
    ''' Test Signin and Signup '''

    def test_user_cannot_register_with_no_data(self):
        ''' Test Signup With No Data '''
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, 400)

    def test_user_can_register_correctly(self):
        ''' Test Correct User Signup '''
        res = self.client.post(
            self.register_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 201)

    def test_user_cannot_login_with_unverified_email(self):
        ''' Test Unverified User Login '''
        res = self.client.post(self.login_url, self.user_data, format="json")
        self.assertEqual(res.status_code, 401)

    def test_user_can_login_after_verification(self):
        ''' Test Verified User Login '''
