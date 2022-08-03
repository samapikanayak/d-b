from datetime import datetime
from django.test import TestCase
from party.models import *
from django.utils import timezone
from random import randint, randrange


# models test
class PartyTypeModelTest(TestCase):

    def create_party_type(self, DE_PRTY_TYP="This is party type one"):
        CD_PRTY_TYP = randint(1000000, 9999999)
        return PartyType.objects.create(CD_PRTY_TYP=CD_PRTY_TYP, DE_PRTY_TYP=DE_PRTY_TYP)

    def test_party_type_creation(self):
        w = self.create_party_type()
        self.assertTrue(isinstance(w, PartyType))
        self.assertEqual(w.__unicode__(), w.CD_PRTY_TYP)


class PartyModelTest(PartyTypeModelTest, TestCase):

    def create_party(self):
        prty_typ_instance = PartyTypeModelTest.create_party_type(self)
        return Party.objects.create(CD_PRTY_TYP=prty_typ_instance)

    def test_party_creation(self):
        w = self.create_party()
        self.assertTrue(isinstance(w, Party))
        self.assertEqual(w.__unicode__(), w.CD_PRTY_TYP)


class PartyRoleModelTest(TestCase):

    def create_party_role(self, NM_RO_PRTY="PARTY_ROLE_1", DE_RO_PRTY="Party Role Description"):
        prty_ro_code = randrange(10000, 99999)
        return PartyRole.objects.create(TY_RO_PRTY=prty_ro_code, NM_RO_PRTY=NM_RO_PRTY, DE_RO_PRTY=DE_RO_PRTY)

    def test_party_role_creation(self):
        w = self.create_party_role()
        self.assertTrue(isinstance(w, PartyRole))
        self.assertEqual(w.__unicode__(), w.NM_RO_PRTY)


class PartyRoleAssgnModelTest(PartyModelTest, PartyTypeModelTest, PartyRoleModelTest, TestCase):

    def create_prty_role_assign(self, ID_PRTY_RO_ASGMT=1):
        prty_role_instance = PartyRoleModelTest.create_party_role(self)

        prty_typ_instance = PartyTypeModelTest.create_party_type(self)
        prty_instance = PartyModelTest.create_party(self)
        return PartyRoleAssignment.objects.create(ID_PRTY=prty_instance, TY_RO_PRTY=prty_role_instance, DC_EF_RO_PRTY=timezone.now(), DC_EP_RO_PRTY=timezone.now())

    def test_party_role_asgn_creation(self):
        w = self.create_prty_role_assign()
        self.assertTrue(w, PartyRoleAssignment)
        self.assertEqual(w.__unicode__(), w.SC_RO_PRTY)


class ContactPurposeTypeModelTest(TestCase):

    def create_cnct_prps_typ(self, CD_TYP_CNCT_PRPS="LG", NM_TYP_CNCT_PRPS="Contact Purpose Type Name"):
        return ContactPurposeType.objects.create(CD_TYP_CNCT_PRPS=CD_TYP_CNCT_PRPS, NM_TYP_CNCT_PRPS=NM_TYP_CNCT_PRPS)

    def test_cnct_prps_type(self):
        w = self.create_cnct_prps_typ()
        self.assertTrue(isinstance(w, ContactPurposeType))
        self.assertEqual(w.__unicode__(), w.NM_TYP_CNCT_PRPS)


class ContactMethodTypeModelTest(TestCase):

    def create_cnct_mth_typ(self, CD_TYP_CNCT_MTH="CTMTH", NM_TYP_CNCT_MTH="Contact Method Type Name"):
        return ContactMethodType.objects.create(CD_TYP_CNCT_MTH=CD_TYP_CNCT_MTH, NM_TYP_CNCT_MTH=NM_TYP_CNCT_MTH)

    def test_cnct_mth_typ(self):
        w = self.create_cnct_mth_typ()
        self.assertTrue(isinstance(w, ContactMethodType))
        self.assertEqual(w.__unicode__(), w.NM_TYP_CNCT_MTH)


class ITUCountryModelTest(TestCase):

    def create_itu_cy_cd(self, NM_CY_ITU="Country Name India"):
        CD_CY_ITU = str(randint(222, 999))
        return ITUCountry.objects.create(CD_CY_ITU=CD_CY_ITU, NM_CY_ITU=NM_CY_ITU)

    def test_itu_cy_cd(self):
        w = self.create_itu_cy_cd()
        self.assertTrue(isinstance(w, ITUCountry))
        self.assertEqual(w.__unicode__(), w.NM_CY_ITU)


class TelephoneModelTest(ITUCountryModelTest, TestCase):

    def create_telephone(self, TA_PH="033", TL_PH="25578", PH_EXTN="123", PH_CMPL="919932047263"):
        itu_instance = ITUCountryModelTest.create_itu_cy_cd(self)
        return Telephone.objects.create(CD_CY_ITU=itu_instance, TA_PH=TA_PH, TL_PH=TL_PH, PH_EXTN=PH_EXTN, PH_CMPL=PH_CMPL)

    def test_itu_cy_cd(self):
        w = self.create_telephone()
        self.assertTrue(isinstance(w, Telephone))
        self.assertEqual(w.__unicode__(), w.PH_CMPL)


class EmailAddressModelTest(TestCase):

    def create_email_address(self, EM_ADS_LOC_PRT="xyz", EM_ADS_DMN_PRT="@abc.in"):
        return EmailAddress.objects.create(EM_ADS_LOC_PRT=EM_ADS_LOC_PRT, EM_ADS_DMN_PRT=EM_ADS_DMN_PRT)

    def test_em_ads_create(self):
        w = self.create_email_address()
        self.assertTrue(isinstance(w, EmailAddress))
        self.assertEqual(w.__unicode__(), w.EM_ADS_LOC_PRT)


class GeographicSegmentModelTest(TestCase):

    def create_geo_sgmt(self, DE_GEO_SGMT_CLSFR="GeographicSegment Description"):
        return GeographicSegment.objects.create(DE_GEO_SGMT_CLSFR=DE_GEO_SGMT_CLSFR)

    def test_geo_sgmt_create(self):
        w = self.create_geo_sgmt()
        self.assertTrue(isinstance(w, GeographicSegment))
        self.assertEqual(w.__unicode__(), w.DE_GEO_SGMT_CLSFR)


class ISO3166CountryModelTest(ITUCountryModelTest, TestCase):

    def create_iso03166_country(self, NM_CY="India", CD_ISO_3CHR_CY="IND"):
        CD_CY_ISO = str(randint(22, 99))
        itu_instance = ITUCountryModelTest.create_itu_cy_cd(self)
        return ISO3166_1Country.objects.create(CD_CY_ISO=CD_CY_ISO, CD_CY_ITU=itu_instance, NM_CY=NM_CY, CD_ISO_3CHR_CY=CD_ISO_3CHR_CY)

    def test_geo_sgmt_create(self):
        w = self.create_iso03166_country()
        self.assertTrue(isinstance(w, ISO3166_1Country))
        self.assertEqual(w.__unicode__(), w.NM_CY)


class PostalCodeRefModelTest(ISO3166CountryModelTest, TestCase):

    def create_pstl_cd_ref(self, CD_PSTL="735301"):
        iso_instance = ISO3166CountryModelTest.create_iso03166_country(self)
        return PostalCodeReference.objects.create(CD_PSTL=CD_PSTL, CD_CY_ISO=iso_instance)

    def test_pstl_cd_ref(self):
        w = self.create_pstl_cd_ref()
        self.assertTrue(isinstance(w, PostalCodeReference))
        self.assertEqual(w.__unicode__(), w.CD_PSTL)


class ISO3166PrimarySubdivisionTypeModelTest(TestCase):

    def create_prmry_sub_typ(self, CD_ISO3166_CY_PRMRY_SBDVN_TYP="ISO3166_SUB", DE_ISO3166_CY_PRMRY_SBDVN_TYP="ISO3166_CountryPrimarySubdivisionDescription"):
        return ISO3166_2PrimarySubdivisionType.objects.create(CD_ISO3166_CY_PRMRY_SBDVN_TYP=CD_ISO3166_CY_PRMRY_SBDVN_TYP, DE_ISO3166_CY_PRMRY_SBDVN_TYP=DE_ISO3166_CY_PRMRY_SBDVN_TYP)

    def test_prmry_sub_typ(self):
        w = self.create_prmry_sub_typ()
        self.assertTrue(isinstance(w, ISO3166_2PrimarySubdivisionType))
        self.assertEqual(w.__unicode__(), w.DE_ISO3166_CY_PRMRY_SBDVN_TYP)


class ISO3166CountrySubdivisionModelTest(ISO3166CountryModelTest, ISO3166PrimarySubdivisionTypeModelTest, TestCase):

    def create_cy_svdvn(self, CD_ISO3166_CY_PRMRY_SBDVN_TYP="ISO3166_SUB", DE_ISO3166_CY_PRMRY_SBDVN_TYP="ISO3166_CountryPrimarySubdivisionDescription"):

        iso_cy_instance = ISO3166CountryModelTest.create_iso03166_country(self)

        iso_prmry_svdn_instance = ISO3166PrimarySubdivisionTypeModelTest.create_prmry_sub_typ(
            self)

        return ISO3166_2CountrySubdivision.objects.create(CD_ISO3166_CY_PRMRY_SBDVN_TYP=iso_prmry_svdn_instance, CD_CY_ISO=iso_cy_instance, ID_ISO_3166_2_CY_PRMRY_SBDVN=1, CD_ISO_3_CHR_CY="IND", NM_ISO_CY_PRMRY_SBDVN="ISOCountryPrimarySubDivisionName", CD_ISO_CY_PRMRY_SBDVN_ABBR_CD="SBDVN", DE_ISO_SBDVN_ALT_NM="ISOSubdivisionAlternateNameDescription", NM_ISO_CY="INDIA")

    def test_prmry_sub_typ(self):
        w = self.create_cy_svdvn()
        self.assertTrue(isinstance(w, ISO3166_2CountrySubdivision))
        self.assertEqual(w.__unicode__(), w.NM_ISO_CY_PRMRY_SBDVN)

#! Address Test Class


class AddressModelTest(GeographicSegmentModelTest, ISO3166CountrySubdivisionModelTest, PostalCodeRefModelTest, TestCase):

    def create_address(self, A1_ADS="Topsia", A2_ADS="Kolkata", A3_ADS="Kolkata", A4_ADS="Kolkata", CI_CNCT="Kolkata", ST_CNCT="West Bengal"):
        geo_instance = GeographicSegmentModelTest.create_geo_sgmt(self)
        cy_svdvn_instance = ISO3166CountrySubdivisionModelTest.create_cy_svdvn(
            self)
        pstl_instance = PostalCodeRefModelTest.create_pstl_cd_ref(self)
        return Address.objects.create(A1_ADS=A1_ADS, A2_ADS=A2_ADS, CI_CNCT=CI_CNCT, ST_CNCT=ST_CNCT, ID_GEO_SGMT=geo_instance, ID_ISO_3166_2_CY_SBDVN=cy_svdvn_instance, ID_PSTL_CD=pstl_instance)

    def test_create_address(self):
        w = self.create_address()
        self.assertTrue(isinstance(w, Address))
        self.assertEqual(w.__unicode__(), w.CI_CNCT)


class SocialNetworkTypeModelTest(TestCase):

    def create_scl_ntwrk_typ(self, DE_SCL_NTWRK_TYP="Social Network Type Description"):
        return SocialNetworkType.objects.create(DE_SCL_NTWRK_TYP=DE_SCL_NTWRK_TYP)

    def test_scl_ntwrk_typ(self):
        w = self.create_scl_ntwrk_typ()
        self.assertTrue(isinstance(w, SocialNetworkType))
        self.assertEqual(w.__unicode__(), w.DE_SCL_NTWRK_TYP)


class WebSiteModelTest(TestCase):

    def create_website(self, URI_HM_PG="Social Network Type Description", NM_WB_STE_BSN="Website Business Name", NM_WB_STE_TTL_TG="Website Tag Value", DE_WB_STE_MTA_DSCR_TG_VL="Meta Description Tag Value", NA_WB_STE_KYWRD_LST="WebSite Meta Keyword List Narrative"):

        return WebSite.objects.create(URI_HM_PG=URI_HM_PG, NM_WB_STE_BSN=NM_WB_STE_BSN, NM_WB_STE_TTL_TG=NM_WB_STE_TTL_TG, DE_WB_STE_MTA_DSCR_TG_VL=DE_WB_STE_MTA_DSCR_TG_VL, NA_WB_STE_KYWRD_LST=NA_WB_STE_KYWRD_LST)

    def test_create_website(self):
        w = self.create_website()
        self.assertTrue(isinstance(w, WebSite))
        self.assertEqual(w.__unicode__(), w.NM_WB_STE_BSN)


class SocialNetworkServiceModelTest(SocialNetworkTypeModelTest, WebSiteModelTest, TestCase):

    def create_scl_ntwrk_service(self, NM_SCL_NTWRK="Facebook"):
        web_insatnce = WebSiteModelTest.create_website(self)
        scl_ntwrk_typ_instance = SocialNetworkTypeModelTest.create_scl_ntwrk_typ(
            self)
        return SocialNetworkService.objects.create(NM_SCL_NTWRK=NM_SCL_NTWRK, CD_SCL_NTWRK_TYP=scl_ntwrk_typ_instance, ID_WB_STE=web_insatnce)

    def test_scl_ntwrk_typ(self):
        w = self.create_scl_ntwrk_service()
        self.assertTrue(isinstance(w, SocialNetworkService))
        self.assertEqual(w.__unicode__(), w.NM_SCL_NTWRK)


class SocialNetworkHandleModelTest(SocialNetworkServiceModelTest, TestCase):

    def create_scl_ntwrk_handle(self, ID_SCL_NTWRK_USR="Haranath"):
        scl_ntwrk_instance = SocialNetworkServiceModelTest.create_scl_ntwrk_service(
            self)
        return SocialNetworkHandle.objects.create(ID_SCL_NTWRK_USR=ID_SCL_NTWRK_USR, ID_SCL_NTWRK=scl_ntwrk_instance)

    def test_scl_ntwrk_handle(self):
        w = self.create_scl_ntwrk_handle()
        self.assertTrue(isinstance(w, SocialNetworkHandle))
        self.assertEqual(w.__unicode__(), w.ID_SCL_NTWRK_USR)


class ConsumerModelTest(PartyRoleAssgnModelTest, PartyModelTest, TestCase):

    def create_consumer(self, ID_CNS="NAVSOFT"):
        prty_instance = PartyModelTest.create_party(self)
        prty_ro_asgmt = PartyRoleAssgnModelTest.create_prty_role_assign(self)
        return Consumer.objects.create(ID_CNS=ID_CNS, ID_PRTY_RO_ASGMT=prty_ro_asgmt, ID_PRTY=prty_instance)

    def test_scl_ntwrk_typ(self):
        w = self.create_consumer()
        self.assertTrue(isinstance(w, Consumer))
        self.assertEqual(w.__unicode__(), w.ID_CNS)


# PartyContactMethod
class PartyContactMethodModelTest(SocialNetworkHandleModelTest, ContactMethodTypeModelTest, ContactPurposeTypeModelTest, PartyRoleAssgnModelTest, WebSiteModelTest, AddressModelTest, EmailAddressModelTest, TelephoneModelTest, TestCase):

    def create_prty_cnct_mth(self, ID_LGE="ENG", NM_LGE="ENGLISH"):
        cnct_prps_typ_instance = ContactPurposeTypeModelTest.create_cnct_prps_typ(
            self)
        cnct_mth_typ_instance = ContactMethodTypeModelTest.create_cnct_mth_typ(
            self)
        prty_ro_asgmt_inst = PartyRoleAssgnModelTest.create_prty_role_assign(
            self)
        scl_ntwrk_hndl_inst = SocialNetworkHandleModelTest.create_scl_ntwrk_handle(
            self)
        ads_instance = AddressModelTest.create_address(self)
        em_ads_instance = EmailAddressModelTest.create_email_address(self)
        ph_instance = TelephoneModelTest.create_telephone(self)
        web_instance = WebSiteModelTest.create_website(self)

        return PartyContactMethod.objects.create(CD_TYP_CNCT_PRPS=cnct_prps_typ_instance, CD_TYP_CNCT_MTH=cnct_mth_typ_instance, ID_PRTY_RO_ASGMT=prty_ro_asgmt_inst, ID_SCL_NTWRK_HNDL=scl_ntwrk_hndl_inst, DC_EF=timezone.now(), DC_EP=timezone.now(), ID_ADS=ads_instance, ID_EM_ADS=em_ads_instance, ID_PH=ph_instance, ID_WB_STE=web_instance)

    def test_prty_cnct_mth(self):
        w = self.create_prty_cnct_mth()
        self.assertTrue(isinstance(w, PartyContactMethod))
        self.assertEqual(w.__unicode__(), w.ID_PRTY_CNCT_MTH)


class LanguageModelTest(TestCase):

    def create_language(self, ID_LGE="ENG", NM_LGE="ENGLISH"):
        return Language.objects.create(ID_LGE=ID_LGE, NM_LGE=NM_LGE)

    def test_create_language(self):
        w = self.create_language()
        self.assertTrue(isinstance(w, Language))
        self.assertEqual(w.__unicode__(), w.NM_LGE)


#! PERSON
class PersonModelTest(PartyModelTest, LanguageModelTest, TestCase):

    def create_person(self):
        prty_instance = PartyModelTest.create_party(self)
        lang_instance = LanguageModelTest.create_language(self)
        return Person.objects.create(ID_PRTY=prty_instance, ID_LGE=lang_instance)

    def test_create_person(self):
        w = self.create_person()
        self.assertTrue(isinstance(w, Person))
        self.assertEqual(w.__unicode__(), w.FN_PRS)


class OperationalPartyModelTest(PartyRoleAssgnModelTest, TestCase):

    def create_opr_prty(self, TY_PRTY_OPR="PR"):
        prty_ro_asgmt = PartyRoleAssgnModelTest.create_prty_role_assign(self)
        return OperationalParty.objects.create(TY_PRTY_OPR=TY_PRTY_OPR, ID_PRTY_RO_ASGMT=prty_ro_asgmt)

    def test_create_opr_prty(self):
        w = self.create_opr_prty()
        self.assertTrue(isinstance(w, OperationalParty))
        self.assertEqual(w.__unicode__(), w.TY_PRTY_OPR)


class LegalOrganizationTypeModelTest(TestCase):

    def create_lgl_org_typ(self, CD_LGL_ORGN_TYP="LG_ORG_TYP", DE_LGL_ORGN_TYP="Legal Organization Type Description"):
        return LegalOrganizationType.objects.create(CD_LGL_ORGN_TYP=CD_LGL_ORGN_TYP, DE_LGL_ORGN_TYP=DE_LGL_ORGN_TYP)

    def test_lgl_org_typ(self):
        w = self.create_lgl_org_typ()
        self.assertTrue(isinstance(w, LegalOrganizationType))
        self.assertEqual(w.__unicode__(), w.DE_LGL_ORGN_TYP)


class OrganizationModelTest(PartyModelTest, LegalOrganizationTypeModelTest, LanguageModelTest, TestCase):

    def create_organization(self):
        org_object = {"NM_LGL": "NAVSOFT", "NM_TRD": "Trade Name", "NM_JRDT_OF_INCRP": "", "MO_LCL_ANN_RVN": 2.4, "MO_GBL_ANN_RVN": 5.5, "ID_DUNS_NBR": "134", "CD_BNKRPTY_TYP": "321", "QU_EM_CNT_LCL": 100, "QU_EM_CNT_GBL": 200, "CD_RTG_DUNN_AND_BRDST": "5",
                      "NA_DE_ORGN": "", "DC_INCRP": timezone.now(), "DC_FSC_YR_END": timezone.now(), "DC_TRMN": timezone.now(), "DC_OPN_FR_BSN":  timezone.now(), "DC_CLSD_FR_BSN": timezone.now(), "DC_BNKRPTY": timezone.now(), "DC_BNKRPTY_EMRGNC": timezone.now()}
        prty_instance = PartyModelTest.create_party(self)
        # lgl_instance = LegalOrganizationTypeModelTest.create_lgl_org_typ(self)
        lang_instance = LanguageModelTest.create_language(self)
        return Organization.objects.create(ID_PRTY=prty_instance, ID_LGE_PRMRY=lang_instance, **org_object)

    def test_create_organization(self):
        w = self.create_organization()
        self.assertTrue(isinstance(w, Organization))
        self.assertEqual(w.__unicode__(), w.ID_ORGN)


class PartyIdentificationTypeModelTest(TestCase):

    def create_prty_idn_type(self, DE_PRTY_ID="LG_ORG_TYP", TY_PRTY_ID="LA"):
        return PartyIdentificationType.objects.create(DE_PRTY_ID=DE_PRTY_ID, TY_PRTY_ID=TY_PRTY_ID)

    def test_prty_idn_typ(self):
        w = self.create_prty_idn_type()
        self.assertTrue(isinstance(w, PartyIdentificationType))
        self.assertEqual(w.__unicode__(), w.TY_PRTY_ID)


class ExtrnlPrtyIdenPrvdrModelTest(PartyRoleAssgnModelTest, TestCase):

    def create_extrn_prvdr(self):
        prty_ro_asgn_instance = PartyRoleAssgnModelTest.create_prty_role_assign(
            self)
        return ExternalPartyIdentificationProvider.objects.create(ID_PRTY_RO_ASGMT=prty_ro_asgn_instance)

    def test_create_extrn_prvdr(self):
        w = self.create_extrn_prvdr()
        self.assertTrue(isinstance(w, ExternalPartyIdentificationProvider))
        self.assertEqual(w.__unicode__(), w.ID_PA_PVR_EXTRN)


class PartyIdentificationModelTest(ExtrnlPrtyIdenPrvdrModelTest, PartyIdentificationTypeModelTest, AddressModelTest, PersonModelTest, PartyModelTest, TestCase):

    def create_lgl_org_typ(self):
        party_instance = PartyModelTest.create_party(self)
        prty_iden_typ_instance = PartyIdentificationTypeModelTest.create_prty_idn_type(
            self)
        person_instance = PersonModelTest.create_person(self)
        ads_instance = AddressModelTest.create_address(self)
        extrn_prvr_instance = ExtrnlPrtyIdenPrvdrModelTest.create_extrn_prvdr(
            self)
        return PartyIdentification.objects.create(ID_PRTY=party_instance, TY_PRTY_ID=prty_iden_typ_instance, DT_EF=timezone.now(), ID_PRTY_PRS=person_instance, ID_ADS=ads_instance, ID_PA_PVR_EXTRN=extrn_prvr_instance, LU_ID_PRTY=1, DC_ISS=timezone.now(), DC_ID_PRTY_EP=timezone.now())

    def test_lgl_org_typ(self):
        w = self.create_lgl_org_typ()
        self.assertTrue(isinstance(w, PartyIdentification))
        self.assertEqual(w.__unicode__(), w.ID_PA_IDTN)
