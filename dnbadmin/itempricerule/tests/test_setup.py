"""
Item Price Rule api test cases setup
"""
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.item_price_rule_get_create = reverse(
            'item_price_rule_get_create')
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "ITM_SL_PRC_STATUS": "A",
            "ITM_SL_PRC_NAME": "Item Selling Price Rule Name",
            "RP_PR_SLS": "3.40",
            "DC_PRC_EF_PRN_RT": "2022-07-14T10:02:06.675000Z",
            "RP_SLS_CRT": "5.90",
            "DC_PRC_SLS_EF_CRT": "2022-07-14T10:02:06.675000Z",
            "RP_PRC_MF_RCM_RT": "5.56",
            "DC_PRC_MF_RCM_RT": "2022-07-14T10:02:06.675000Z",
            "QU_PCKG_PRC_CRT": "78",
            "RP_PCKG_PRC_CRT": "4.00",
            "RP_RTN_UN_CRT_SLS": "5.00",
            "QU_PCKG_PRC_PRN": "6",
            "RP_RTN_UN_PRN_SLS": "7.00",
            "MO_AMT_TX_PRN": "7.00",
            "RP_MNM_ADVRTSD": "8.00",
            "DC_EF_RP_MNM_ADVRTSD": "2022-07-14T10:02:06.675000Z",
            "FL_MKD_ORGL_PRC_PR": 1,
            "FL_QTY_PRC": 1,
            "FL_TX_INC": 1
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
