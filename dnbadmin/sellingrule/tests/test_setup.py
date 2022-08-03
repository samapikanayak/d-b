"""
selling rule api test cases setup
"""
from django.utils import timezone
from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    ''' Test Setup '''

    def setUp(self):
        ''' Here we setup data for unit test '''
        self.register_url = reverse('signup')
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        self.setting_data = {
            "NM_RU_ITM_SL": 'Test selling rule',
            "DE_RU_ITM_SL": 'Test Description',
            "status": "A",
            "DC_ITM_SLS": timezone.now(),
            "expired_date": timezone.now(),
            "QU_MNM_SLS_UN": 22,
            "QU_UN_BLK_MXM": 22,
            "FL_CPN_RST": 22,
            "FL_CPN_ELTNC": 22,
            "FL_ENR_PRC_RQ": 22,
            "FL_DSC_EM_ALW": 22,
            "FL_FD_STP_ALW": 22,
            "FL_CPN_ALW_MULTY": 2,
            "FL_KY_PRH_RPT": 2,
            "FL_ENT_WT_RQ": 222,
            "FL_PRC_VS_VR": 222,
            "FL_PNT_FQ_SHPR": 1,
            "QU_PNT_FQ_SHPR": "hh",
            "CD_QTY_ACTN_KY": 5,
            "FL_RTN_PRH": 5,
            "FL_ITM_WIC": 5,
            "FL_ITM_GWY": 5,
            "FL_RNCHK_EL": 5,
            "FL_PRPPRTNL_RFD_EL": 5
        }

        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
