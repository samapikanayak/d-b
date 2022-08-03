'''selling rule model test'''
from django.test import TestCase
from sellingrule.models import ItemTenderRestrictionGroup, ItemSellingRule
from depositrule.tests import test_models
from django.utils import timezone


class ItemTenderRestrictionGroupTest(TestCase):
    '''Item Tender Restriction Test cases'''

    def create_item_tender_restriction_group(self):
        '''item tender restriction create test cases'''
        DE_GP_TND_RST = "Description"
        NA_GP_TND_RST = "na_gp_tnd_rst"
        return ItemTenderRestrictionGroup.objects.create(DE_GP_TND_RST=DE_GP_TND_RST, NA_GP_TND_RST=NA_GP_TND_RST)

    def test_item_tender_restriction_group(self):
        '''item tender restriction model test cases'''
        w = self.create_item_tender_restriction_group()
        self.assertTrue(isinstance(w, ItemTenderRestrictionGroup))


class ItemSellingRuleTest(TestCase):

    def create_item_selling_rule(self):
        return ItemSellingRule.objects.create(NM_RU_ITM_SL='Test selling rule', DE_RU_ITM_SL='Test Description', ID_RU_DS=test_models.DepositRuleModelTest.create_deposit_rule(self), status="A", DC_ITM_SLS=timezone.now(), expired_date=timezone.now(), FL_CPN_RST=2, FL_CPN_ELTNC=2, FL_ENR_PRC_RQ=2, FL_ENT_WT_RQ=2, QU_MNM_SLS_UN=2, QU_UN_BLK_MXM=2, FL_DSC_EM_ALW=2, FL_FD_STP_ALW=2, FL_CPN_ALW_MULTY=2, FL_KY_PRH_RPT=2, FL_PRC_VS_VR=2, FL_PNT_FQ_SHPR=2, QU_PNT_FQ_SHPR=2.2, CD_QTY_ACTN_KY='A', FL_RTN_PRH=2, FL_ITM_WIC=2, FL_ITM_GWY=2, FL_RNCHK_EL=2, FL_PRPPRTNL_RFD_EL=2
                                              )

    def test_item_selling_rule(self):
        w = self.create_item_selling_rule()
        self.assertTrue(isinstance(w, ItemSellingRule))
