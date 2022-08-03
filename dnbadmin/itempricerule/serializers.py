''' Item Price Rule Serializer '''
import logging
from rest_framework import serializers
from product.models import ItemSellingPrices

logger = logging.getLogger(__name__)


class ItemPriceRuleSerializer(serializers.ModelSerializer):
    ''' Item Price Rule Serializer '''

    class Meta:
        ''' This is a Meta Class'''
        model = ItemSellingPrices
        fields = ['ID_ITM_SL_PRC', 'ITM_SL_PRC_STATUS',
                  'ITM_SL_PRC_NAME', 'RP_PR_SLS', 'DC_PRC_EF_PRN_RT', 'RP_SLS_CRT', 'DC_PRC_SLS_EF_CRT', 'RP_PRC_MF_RCM_RT',
                  'DC_PRC_MF_RCM_RT', 'QU_PCKG_PRC_CRT', 'RP_PCKG_PRC_CRT', 'RP_RTN_UN_CRT_SLS', 'QU_PCKG_PRC_PRN', 'RP_RTN_UN_PRN_SLS', 'MO_AMT_TX_PRN',
                  'RP_MNM_ADVRTSD', 'DC_EF_RP_MNM_ADVRTSD',
                  'FL_MKD_ORGL_PRC_PR', 'FL_QTY_PRC', 'FL_TX_INC']
