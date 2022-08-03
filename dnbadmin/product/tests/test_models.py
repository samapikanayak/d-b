import imp
from django.test import TestCase
from ..models import *
from django.utils.crypto import get_random_string as grs
from django.utils import timezone
from random import randint
from taxonomy.tests.test_models import MerchandiseHierarchyGroupTest
from sellingrule.tests.test_models import ItemSellingRuleTest
from brand.tests.test_models import BrandModelTest, SubBrandModelTest
from store.tests.test_models import BusinessUnitGroupModelTest


class ItemSellingPricesTest(TestCase):
    def create_item_selling_prices_test(self):
        RP_PR_SLS = 12.66
        FL_MKD_ORGL_PRC_PR = randint(1,10000)
        QU_MKD_PR_PRC_PR = 10.35
        DC_PRC_EF_PRN_RT = timezone.now()
        RP_SLS_CRT = 12.224
        TY_PRC_RT = grs(2)
        FL_PRC_RT_PNT_ALW = randint(1,10000)
        DC_PRC_SLS_EF_CRT = timezone.now()
        DC_PRC_SLS_EP_CRT = timezone.now()
        RP_PRC_MF_RCM_RT = 55.215
        DC_PRC_MF_RCM_RT = timezone.now()
        RP_PRC_CMPR_AT_SLS = 55.22
        FL_QTY_PRC = randint(1,10000)
        QU_PCKG_PRC_CRT = 12.22
        RP_PCKG_PRC_CRT = 12.22
        QU_PCKG_PRC_PRN = 12.22
        RP_PCKG_PRC_PRN = 12.22
        RP_RTN_UN_PRN_SLS = 12.22
        RP_RTN_UN_CRT_SLS = 12.22
        FL_TX_INC = randint(1,10000)
        MO_AMT_TX_PRN = 12.22
        MO_AMT_TX_CRT = 12.22
        RP_MNM_ADVRTSD = 12.22
        DC_EF_RP_MNM_ADVRTSD = timezone.now()

        return ItemSellingPrices.objects.create(RP_PR_SLS=RP_PR_SLS, FL_MKD_ORGL_PRC_PR=FL_MKD_ORGL_PRC_PR, QU_MKD_PR_PRC_PR=QU_MKD_PR_PRC_PR, DC_PRC_EF_PRN_RT=DC_PRC_EF_PRN_RT, RP_SLS_CRT=RP_SLS_CRT, TY_PRC_RT=TY_PRC_RT, FL_PRC_RT_PNT_ALW=FL_PRC_RT_PNT_ALW, DC_PRC_SLS_EF_CRT=DC_PRC_SLS_EF_CRT, DC_PRC_SLS_EP_CRT=DC_PRC_SLS_EP_CRT, RP_PRC_MF_RCM_RT=RP_PRC_MF_RCM_RT, DC_PRC_MF_RCM_RT=DC_PRC_MF_RCM_RT, RP_PRC_CMPR_AT_SLS=RP_PRC_CMPR_AT_SLS, FL_QTY_PRC=FL_QTY_PRC, QU_PCKG_PRC_CRT=QU_PCKG_PRC_CRT, RP_PCKG_PRC_CRT=RP_PCKG_PRC_CRT, QU_PCKG_PRC_PRN=QU_PCKG_PRC_PRN, RP_PCKG_PRC_PRN=RP_PCKG_PRC_PRN, RP_RTN_UN_PRN_SLS=RP_RTN_UN_PRN_SLS, RP_RTN_UN_CRT_SLS=RP_RTN_UN_CRT_SLS, FL_TX_INC=FL_TX_INC, MO_AMT_TX_PRN=MO_AMT_TX_PRN, MO_AMT_TX_CRT=MO_AMT_TX_CRT, RP_MNM_ADVRTSD=RP_MNM_ADVRTSD, DC_EF_RP_MNM_ADVRTSD=DC_EF_RP_MNM_ADVRTSD)

    def test_item_selling_prices_test(self):
        w = self.create_item_selling_prices_test()
        self.assertTrue(isinstance(w, ItemSellingPrices))


class PriceLineTest(TestCase):
    def create_price_line(self):
        ID_MRHRC_GP = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(self)
        LL_LN_PRC = 12.235
        UL_LN_PRC = 12.1544
        return PriceLine.objects.create(ID_MRHRC_GP=ID_MRHRC_GP, LL_LN_PRC=LL_LN_PRC, UL_LN_PRC=UL_LN_PRC)

    def test_price_line(self):
        w = self.create_price_line()
        self.assertTrue(isinstance(w, PriceLine))

class POSDepartmentTest(TestCase):
    def create_pos_department(self):
        ID_RU_ITM_SL = ItemSellingRuleTest.create_item_selling_rule(self)
        NM_DPT_PS = "Name"

        return POSDepartment.objects.create(ID_RU_ITM_SL=ID_RU_ITM_SL, NM_DPT_PS=NM_DPT_PS)

    def create_if_table_exists(self):
        ID_RU_ITM_SL = ItemSellingRuleTest.create_item_selling_rule(self)
        NM_DPT_PS = "Name"
        ID_DPT_PS_PRNT = self.create_pos_department()
        return POSDepartment.objects.create(ID_RU_ITM_SL=ID_RU_ITM_SL, NM_DPT_PS=NM_DPT_PS, ID_DPT_PS_PRNT=ID_DPT_PS_PRNT)

    def test_pos_department(self):
        w = self.create_if_table_exists()
        self.assertTrue(isinstance(w, POSDepartment))

class ItemTest(TestCase):
    def create_item(self):
        ID_MRHRC_GP = MerchandiseHierarchyGroupTest.create_merchandise_hierarchy_group(self)
        ID_ITM_SL_PRC = ItemSellingPricesTest.create_item_selling_prices_test(self)
        ID_RU_ITM_SL = ItemSellingRuleTest.create_item_selling_rule(self)
        ID_DPT_PS = POSDepartmentTest.create_pos_department(self)
        ID_LN_PRC = PriceLineTest.create_price_line(self)
        NM_BRN = BrandModelTest.create_brand(self)
        FL_AZN_FR_SLS = randint(1,10000)
        FL_ITM_DSC = randint(1,1000)
        FL_ADT_ITM_PRC = randint(1,1000)
        LU_EXM_TX = grs(2)
        LU_ITM_USG = grs(2)
        NM_ITM = grs(40)
        DE_ITM = grs(255)
        DE_ITM_LNG = grs(255)
        TY_ITM = grs(4)
        LU_KT_ST = grs(2)
        FL_ITM_SBST_IDN = randint(0,200)
        LU_CLN_ORD = grs(2)
        FL_VLD_SRZ_ITM = randint(0,200)
        AI_SUB_BRN = SubBrandModelTest.create_sub_brand(self)
        NM_BRN_SUB_BRN = grs(40)
        return Item.objects.create(ID_MRHRC_GP=ID_MRHRC_GP, ID_ITM_SL_PRC=ID_ITM_SL_PRC, ID_RU_ITM_SL=ID_RU_ITM_SL, ID_DPT_PS=ID_DPT_PS, NM_BRN=NM_BRN, FL_AZN_FR_SLS=FL_AZN_FR_SLS, FL_ITM_DSC=FL_ITM_DSC, FL_ADT_ITM_PRC=FL_ADT_ITM_PRC, LU_EXM_TX=LU_EXM_TX, LU_ITM_USG=LU_ITM_USG, NM_ITM=NM_ITM, DE_ITM=DE_ITM, DE_ITM_LNG=DE_ITM_LNG, TY_ITM=TY_ITM, LU_KT_ST=LU_KT_ST, FL_ITM_SBST_IDN=FL_ITM_SBST_IDN, LU_CLN_ORD=LU_CLN_ORD, FL_VLD_SRZ_ITM=FL_VLD_SRZ_ITM, AI_SUB_BRN=AI_SUB_BRN, NM_BRN_SUB_BRN=NM_BRN_SUB_BRN, ID_LN_PRC=ID_LN_PRC)
        

    def test_item(self):
        w = self.create_item()
        self.assertTrue(isinstance(w, Item))

class BusinessUnitGroupItemTest(TestCase):
    def create_business_unit_group_item(self):
        ID_BSNGP = BusinessUnitGroupModelTest.create_business_unit_grp(self)
        ID_ITM = ItemTest.create_item(self)
        TS_EF = timezone.now()
        TS_EP = timezone.now()
        ID_ITM_SL_PRC = ItemSellingPricesTest.create_item_selling_prices_test(self)
        ID_RU_ITM_SL = ItemSellingRuleTest.create_item_selling_rule(self)
        SC_ITM_SLS = grs(2)
        SC_ITM = grs(2)
        DC_ITM_SLS = timezone.now()
        FL_STK_UPDT_ON_HD = randint(1,1000)

        return BusinessUnitGroupItem.objects.create(ID_BSNGP=ID_BSNGP, ID_ITM=ID_ITM, TS_EF=TS_EF, TS_EP=TS_EP, ID_ITM_SL_PRC=ID_ITM_SL_PRC, ID_RU_ITM_SL=ID_RU_ITM_SL, SC_ITM_SLS=SC_ITM_SLS, SC_ITM=SC_ITM, DC_ITM_SLS=DC_ITM_SLS, FL_STK_UPDT_ON_HD=FL_STK_UPDT_ON_HD)

    def test_business_unit_group_item(self):
        w = self.create_business_unit_group_item()
        self.assertTrue(isinstance(w, BusinessUnitGroupItem))







