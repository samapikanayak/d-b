from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string

STATUS_CHOICES = (
    ("A", "Active"),
    ("I", "Inactive")
)
CONTACT_PURPOSE_CHOICES = (
    ("LG", "LEGAL"),
    ("BL", "BILLING"),
    ("ST", "SHIP_TO"),
    ("OR", "OTHER"),
    ("SA", "SALES_ANALYSIS")
)
REG_STATE_CHOICES = (
    ("REGISTERED_VALIDATED", "REGISTERED VALIDATED"),
    ("REGISTERED_UNVALIDATE", "REGISTERED UNVALIDATE"),
    ("UNREGISTERED", "UNREGISTERED")
)
REG_ACTION_CHOICES = (
    ("CREATE", "CREATE"),
    ("VALIDATE", "VALIDATE"),
    ("CANCEL", "CANCEL")
)
# Create your models here.


class PartyType(models.Model):
    CD_PRTY_TYP = models.CharField(
        "PartyType Code", primary_key=True, max_length=20)
    DE_PRTY_TYP = models.CharField(
        "PartyType Description", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'LU_PA_TYP'

    def __unicode__(self):
        return self.CD_PRTY_TYP


class Party(models.Model):
    ID_PRTY = models.BigAutoField("Party ID", primary_key=True)
    CD_PRTY_TYP = models.ForeignKey(
        PartyType, on_delete=models.CASCADE, verbose_name="Party Type", db_column="CD_PRTY_TYP")

    class Meta:
        db_table = 'PA_PRTY'

    def __unicode__(self):
        return self.CD_PRTY_TYP


class PartyRole(models.Model):
    TY_RO_PRTY = models.CharField(
        "PartyRole Type Code", primary_key=True, max_length=6)
    NM_RO_PRTY = models.CharField("Name", max_length=40)
    DE_RO_PRTY = models.TextField("Description", blank=True, null=True)

    class Meta:
        db_table = 'PA_RO_PRTY_TYP'

    def __unicode__(self):
        return self.NM_RO_PRTY


class PartyRoleAssignment(models.Model):
    ID_PRTY_RO_ASGMT = models.BigAutoField(
        "PartyRoleAssignment ID", primary_key=True)
    ID_PRTY = models.ForeignKey(
        Party, on_delete=models.CASCADE, verbose_name="Party ID", db_column="ID_PRTY")
    TY_RO_PRTY = models.ForeignKey(PartyRole, on_delete=models.CASCADE,
                                   verbose_name="PartyRole Type Code", db_column="TY_RO_PRTY")
    SC_RO_PRTY = models.CharField(
        "Status Code", max_length=2, choices=STATUS_CHOICES, default="A")
    DC_EF_RO_PRTY = models.DateTimeField("Effective Date")
    DC_EP_RO_PRTY = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'PA_RO_PRTY'

    def __unicode__(self):
        return self.SC_RO_PRTY


class ContactPurposeType(models.Model):
    CD_TYP_CNCT_PRPS = models.CharField(
        "ContactPurpose Type Code", primary_key=True, max_length=2)
    NM_TYP_CNCT_PRPS = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'CO_TYP_CNCT_PRPS'

    def __str__(self):
        return self.NM_TYP_CNCT_PRPS

    def __unicode__(self):
        return self.NM_TYP_CNCT_PRPS


class ContactMethodType(models.Model):
    CD_TYP_CNCT_MTH = models.CharField(
        "ContactMethod Type Code", primary_key=True, max_length=6)
    NM_TYP_CNCT_MTH = models.CharField("Contact Method Name", max_length=40)

    class Meta:
        db_table = 'CO_TYP_CNCT_MTH'

    def __str__(self):
        return self.NM_TYP_CNCT_MTH

    def __unicode__(self):
        return self.NM_TYP_CNCT_MTH


class ITUCountry(models.Model):
    CD_CY_ITU = models.CharField(
        "ITU Country Code", primary_key=True, max_length=3)
    NM_CY_ITU = models.CharField("ITU Country Name", max_length=40)

    class Meta:
        db_table = 'LO_CY_ITU'
        verbose_name = "ITUCountry"
        verbose_name_plural = "ITUCountries"

    def __str__(self):
        return self.NM_CY_ITU

    def __unicode__(self):
        return self.NM_CY_ITU

    def save(self, *args, **kwargs):
        if not self.CD_CY_ITU:
            self.CD_CY_ITU = get_random_string(3)
            if ITUCountry.objects.filter(CD_CY_ITU=self.CD_CY_ITU).exists():
                self.CD_CY_ITU = get_random_string(3)
        return super(ITUCountry, self).save(*args, **kwargs)


class Telephone(models.Model):
    ID_PH = models.BigAutoField("Telephone ID", primary_key=True)
    CD_CY_ITU = models.ForeignKey(
        ITUCountry, on_delete=models.CASCADE, verbose_name="ITU Country Code", db_column="CD_CY_ITU")
    TA_PH = models.CharField("AreaCode", max_length=5)
    TL_PH = models.CharField("TelephoneNumber", max_length=20)
    PH_EXTN = models.CharField(
        "ExtensionNumber", max_length=5, blank=True, null=True)
    PH_CMPL = models.CharField("CompleteNumber", max_length=32)

    class Meta:
        db_table = 'LO_PH'

    def __unicode__(self):
        return self.PH_CMPL


class EmailAddress(models.Model):
    ID_EM_ADS = models.BigAutoField("EmailAddress ID", primary_key=True)
    EM_ADS_LOC_PRT = models.CharField(
        "Email Address Local Part", max_length=253)
    EM_ADS_DMN_PRT = models.CharField(
        "Email Address Domain Part", max_length=253)

    class Meta:
        db_table = 'LO_EML_ADS'

    def __unicode__(self):
        return self.EM_ADS_LOC_PRT


class GeographicSegment(models.Model):
    ID_GEO_SGMT = models.BigAutoField("GeographicSegment ID", primary_key=True)
    DE_GEO_SGMT_CLSFR = models.CharField(
        "GeographicSegment Description", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'CO_GEO_SGMT'

    def __unicode__(self):
        return self.DE_GEO_SGMT_CLSFR


class ISO3166_1Country(models.Model):
    CD_CY_ISO = models.CharField(
        "ISOCountryCode", primary_key=True, max_length=2)
    CD_CY_ITU = models.ForeignKey(
        ITUCountry, on_delete=models.CASCADE, verbose_name="ITU Country Code", db_column="CD_CY_ITU")
    NM_CY = models.CharField("CountryName", max_length=40)
    CD_ISO_3CHR_CY = models.CharField(
        "Three Character CountryCode", max_length=4, blank=True, null=True)

    class Meta:
        db_table = 'LO_CY_ISO'
        verbose_name = "ISO3166_1Country"
        verbose_name_plural = "ISO3166_1Countries"

    def __str__(self):
        return self.NM_CY

    def __unicode__(self):
        return self.NM_CY

    def save(self, *args, **kwargs):
        if not self.CD_CY_ISO:
            self.CD_CY_ISO = get_random_string(2)
            if ISO3166_1Country.objects.filter(CD_CY_ISO=self.CD_CY_ISO).exists():
                self.CD_CY_ISO = get_random_string(2)
        return super(ISO3166_1Country, self).save(*args, **kwargs)


class PostalCodeReference(models.Model):
    ID_PSTL_CD = models.BigAutoField("PostalCode ID", primary_key=True)
    CD_PSTL = models.CharField("PostalCode", max_length=20)
    CD_CY_ISO = models.ForeignKey(ISO3166_1Country, on_delete=models.CASCADE,
                                  verbose_name="ITU Country Code", db_column="CD_CY_ISO")
    DE_PSTL_CD = models.CharField(
        "PostalCode Description", max_length=255, blank=True, null=True)
    CD_PSTL_EXTN = models.CharField(
        "PostalCode Extension", max_length=4, blank=True, null=True)

    class Meta:
        db_table = 'LU_PSTL_CD_RFC'

    def __unicode__(self):
        return self.CD_PSTL


class ISO3166_2PrimarySubdivisionType(models.Model):
    CD_ISO3166_CY_PRMRY_SBDVN_TYP = models.CharField(
        "ISO3166_CountryPrimarySubdivisionTypeCode", primary_key=True, max_length=20)
    DE_ISO3166_CY_PRMRY_SBDVN_TYP = models.CharField(
        "ISO3166_CountryPrimarySubdivisionDescription", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'LU_ISO3166_2_PRMRY_SBDVN_TYP'
        verbose_name = "ISO3166_2PrimarySubdivisionType"

    def __str__(self):
        return self.CD_ISO3166_CY_PRMRY_SBDVN_TYP

    def __unicode__(self):
        return self.DE_ISO3166_CY_PRMRY_SBDVN_TYP


class ISO3166_2CountrySubdivision(models.Model):
    ID_ISO_3166_2_CY_SBDVN = models.BigAutoField(
        "ISO_3166_2CountrySubDivisionID", primary_key=True)
    ID_ISO_3166_2_CY_PRMRY_SBDVN = models.IntegerField(
        "ISOCountryPrimarySubdivisionID", unique=True,)
    CD_ISO_3_CHR_CY = models.CharField(
        "ISOThreeCharacterCountryCode", max_length=4)
    NM_ISO_CY_PRMRY_SBDVN = models.CharField(
        "ISOCountryPrimarySubDivisionName", max_length=40)
    CD_ISO_CY_PRMRY_SBDVN_ABBR_CD = models.CharField(
        "ISOCountryPrimarySubDivisionAbbreviationCode", max_length=6, blank=True, null=True)
    DE_ISO_SBDVN_ALT_NM = models.CharField(
        "ISOSubdivisionAlternateNameDescription", max_length=255, blank=True, null=True)
    NM_ISO_CY = models.CharField("ISOCountryName", max_length=40)
    CD_ISO3166_CY_PRMRY_SBDVN_TYP = models.ForeignKey(ISO3166_2PrimarySubdivisionType, on_delete=models.CASCADE,
                                                      verbose_name="ISO3166_CountryPrimarySubdivisionTypeCode", db_column="CD_ISO3166_CY_PRMRY_SBDVN_TYP")
    CD_CY_ISO = models.ForeignKey(ISO3166_1Country, on_delete=models.CASCADE,
                                  verbose_name="ISOCountryCode", db_column="CD_CY_ISO")

    class Meta:
        db_table = 'CO_ISO3166_2_PRMRY_SBDVN'
        verbose_name = "ISO3166_2CountrySubdivision"

    def __str__(self):
        return self.NM_ISO_CY_PRMRY_SBDVN

    def __unicode__(self):
        return self.NM_ISO_CY_PRMRY_SBDVN


class Address(models.Model):
    ID_ADS = models.BigAutoField("Address ID", primary_key=True)
    A1_ADS = models.CharField("AddressLine1", max_length=80)
    A2_ADS = models.CharField(
        "AddressLine2", max_length=80, blank=True, null=True)
    A3_ADS = models.CharField(
        "AddressLine3", max_length=80, blank=True, null=True)
    A4_ADS = models.CharField(
        "AddressLine4", max_length=80, blank=True, null=True)
    CI_CNCT = models.CharField("City", max_length=30)
    ST_CNCT = models.CharField("State", max_length=30)
    ID_GEO_SGMT = models.ForeignKey(GeographicSegment, on_delete=models.CASCADE,
                                    verbose_name="Geographic Segment ID", blank=True, null=True, db_column="ID_GEO_SGMT")
    ID_ISO_3166_2_CY_SBDVN = models.ForeignKey(ISO3166_2CountrySubdivision, on_delete=models.CASCADE,
                                               verbose_name="CountrySubdivision", blank=True, null=True, db_column="ID_ISO_3166_2_CY_SBDVN")
    ID_PSTL_CD = models.ForeignKey(PostalCodeReference, on_delete=models.CASCADE,
                                   verbose_name="Postal Code ID", blank=True, null=True, db_column="ID_PSTL_CD")

    class Meta:
        db_table = 'LO_ADS'

    def __unicode__(self):
        return self.CI_CNCT


class SocialNetworkType(models.Model):
    CD_SCL_NTWRK_TYP = models.CharField(
        "SocialNetworkTypeCode", primary_key=True, max_length=20)
    DE_SCL_NTWRK_TYP = models.CharField(
        "SocialNetworkTypeDescription", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'LU_SCL_NTWRK_TYP'

    def __unicode__(self):
        return self.DE_SCL_NTWRK_TYP


class WebSite(models.Model):
    ID_WB_STE = models.BigAutoField("WebSiteID", primary_key=True)
    URI_HM_PG = models.CharField("HomePageURIName", max_length=255)
    NM_WB_STE_BSN = models.CharField("WebSiteBusinessName", max_length=255)
    NM_WB_STE_TTL_TG = models.CharField(
        "WebSiteTitleTagValue", max_length=255, blank=True, null=True)
    DE_WB_STE_MTA_DSCR_TG_VL = models.CharField(
        "WebSiteMetaDescriptionTagValue", max_length=255, blank=True, null=True)
    NA_WB_STE_KYWRD_LST = models.TextField(
        "WebSiteMetaKeywordListNarrative", blank=True, null=True)

    class Meta:
        db_table = 'LO_WB_STE'

    def __unicode__(self):
        return self.NM_WB_STE_BSN


class SocialNetworkService(models.Model):
    ID_SCL_NTWRK = models.BigAutoField("SocialNetworkID", primary_key=True)
    NM_SCL_NTWRK = models.CharField("SocialNetworkName", max_length=40)
    CD_SCL_NTWRK_TYP = models.ForeignKey(
        SocialNetworkType, on_delete=models.CASCADE, verbose_name="SocialNetworkTypeCode", db_column="CD_SCL_NTWRK_TYP")
    ID_WB_STE = models.ForeignKey(
        WebSite, on_delete=models.CASCADE, verbose_name="WebSiteID", db_column="ID_WB_STE")

    class Meta:
        db_table = 'PA_SCL_NTWRK'

    def __unicode__(self):
        return self.NM_SCL_NTWRK


class SocialNetworkHandle(models.Model):
    ID_SCL_NTWRK_HNDL = models.BigAutoField(
        "SocialNetworkUserID", primary_key=True)
    ID_SCL_NTWRK_USR = models.CharField("UserProfileID", max_length=255)
    ID_SCL_NTWRK = models.ForeignKey(
        SocialNetworkService, on_delete=models.CASCADE, verbose_name="SocialNetworkID", db_column="ID_SCL_NTWRK")

    class Meta:
        db_table = 'PA_SCL_NTWRK_HNDL'

    def __unicode__(self):
        return self.ID_SCL_NTWRK_USR


class Consumer(models.Model):
    ID_CNS = models.CharField("SocialNetworkTypeCode",
                              primary_key=True, max_length=20)
    ID_PRTY_RO_ASGMT = models.ForeignKey(
        PartyRoleAssignment, on_delete=models.CASCADE, verbose_name="PartyRoleAssignmentID", db_column="ID_PRTY_RO_ASGMT")
    ID_PRTY = models.ForeignKey(
        Party, on_delete=models.CASCADE, verbose_name="PartyID", db_column="ID_PRTY")

    class Meta:
        db_table = 'PA_CNS'

    def __unicode__(self):
        return self.ID_CNS


class PartyContactMethod(models.Model):
    ID_PRTY_CNCT_MTH = models.BigAutoField(
        "PartyContactMethodID", primary_key=True)
    CD_TYP_CNCT_PRPS = models.ForeignKey(ContactPurposeType, on_delete=models.CASCADE,
                                         verbose_name="ContactPurposeTypeCode", db_column="CD_TYP_CNCT_PRPS")
    CD_TYP_CNCT_MTH = models.ForeignKey(ContactMethodType, on_delete=models.CASCADE,
                                        verbose_name="ContactMethodTypeCode", db_column="CD_TYP_CNCT_MTH")
    ID_PRTY_RO_ASGMT = models.ForeignKey(
        PartyRoleAssignment, on_delete=models.CASCADE, verbose_name="PartyRoleAssignmentID", db_column="ID_PRTY_RO_ASGMT")
    ID_SCL_NTWRK_HNDL = models.ForeignKey(
        SocialNetworkHandle, on_delete=models.CASCADE, verbose_name="SocialNetworkUserID", db_column="ID_SCL_NTWRK_HNDL")
    DC_EF = models.DateTimeField("EffectiveDateTime")
    DC_EP = models.DateTimeField("ExpirationDateTime")
    ID_ADS = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name="AddressID", db_column="ID_ADS")
    ID_EM_ADS = models.ForeignKey(
        EmailAddress, on_delete=models.CASCADE, verbose_name="EmailAddressID", db_column="ID_EM_ADS")
    ID_PH = models.ForeignKey(
        Telephone, on_delete=models.CASCADE, verbose_name="TelephoneID", db_column="ID_PH")
    ID_WB_STE = models.ForeignKey(
        WebSite, on_delete=models.CASCADE, verbose_name="WebSiteID", db_column="ID_WB_STE")
    CD_STS = models.CharField(
        "StatusCode", max_length=2, choices=STATUS_CHOICES, default="A")
    # ID_CNS_RGSTN_ST = models.ForeignKey(ConsumerRegistrationState,on_delete=models.CASCADE,verbose_name="ConsumerRegistrationStateID")  # NOSONAR
    PCM_CRT_DT = models.DateTimeField("Created Date", auto_now_add=True)
    PCM_CRT_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='PC_Createuser', db_column="PCM_CRT_BY")
    PCM_MDF_DT = models.DateTimeField("Modified Date", auto_now=True)
    PCM_MDF_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='PC_Modifiyuser', db_column="PCM_MDF_BY")

    class Meta:
        db_table = 'CO_MTH_CNCT_PTY'

    def __unicode__(self):
        return self.ID_PRTY_CNCT_MTH


class Language(models.Model):
    ID_LGE = models.CharField("LanguageID", primary_key=True, max_length=4)
    NM_LGE = models.CharField("Name", max_length=40)

    class Meta:
        db_table = 'CO_LGE'

    def __unicode__(self):
        return self.NM_LGE


class Person(models.Model):
    ID_PRTY_PRS = models.BigAutoField("PersonPartyID", primary_key=True)
    ID_PRTY = models.ForeignKey(
        Party, on_delete=models.CASCADE, verbose_name="Party ID", db_column="ID_PRTY")
    ID_LGE = models.ForeignKey(Language, on_delete=models.SET_NULL,
                               verbose_name="LanguageID", blank=True, null=True, db_column="ID_LGE")
    NM_PRS_SLN = models.CharField(
        "Salutation", max_length=40, blank=True, null=True)
    FN_PRS = models.CharField("FirstName", max_length=40)
    TY_NM_FS = models.CharField(
        "FirstNameType", max_length=2, blank=True, null=True)
    MD_PRS = models.CharField(
        "MiddleNames", max_length=40, blank=True, null=True)
    TY_NM_MID = models.CharField(
        "MiddleNameType", max_length=2, blank=True, null=True)
    LN_PRS = models.CharField("LastName", max_length=40)
    TY_NM_LS = models.CharField(
        "LastNameType", max_length=2, blank=True, null=True)
    NM_PRS_SFX = models.CharField(
        "Suffix", max_length=40, blank=True, null=True)
    TY_GND_PRS = models.CharField(
        "GenderTypeCode", max_length=2, blank=True, null=True)
    NM_PRS_SR = models.CharField("SortingName", max_length=40)
    NM_PRS_ML = models.CharField("MailingName", max_length=40)
    NM_PRS_OFCL = models.CharField("OfficialName", max_length=40)
    PRS_CRT_DT = models.DateTimeField("Created Date", auto_now_add=True)
    PRS_CRT_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='PRS_Createuser', db_column="PRS_CRT_BY")
    PRS_MDF_DT = models.DateTimeField("Modified Date", auto_now=True)
    PRS_MDF_BY = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   blank=True, null=True, related_name='PRS_Modifiyuser', db_column="PRS_MDF_BY")

    class Meta:
        db_table = 'PA_PRS'

    def __unicode__(self):
        return self.FN_PRS


class OperationalParty(models.Model):
    ID_OPR_PRTY = models.BigAutoField("OperationalPartyID", primary_key=True)
    TY_PRTY_OPR = models.CharField("OperatingPartyTypeCode", max_length=2)
    ID_PRTY_RO_ASGMT = models.ForeignKey(
        PartyRoleAssignment, on_delete=models.CASCADE, verbose_name="PartyRoleAssignmentID", db_column="ID_PRTY_RO_ASGMT")

    class Meta:
        db_table = 'PA_PRTY_OPR'

    def __unicode__(self):
        return self.TY_PRTY_OPR


class LegalOrganizationType(models.Model):
    """ Legal Organization Type Model Class """
    CD_LGL_ORGN_TYP = models.CharField(
        "LegalOrgnizationTypeCode", max_length=40, primary_key=True)
    # ID_LGL_ORGN_TYP = models.BigAutoField(
    #     "LegalOrganizationTypeID", primary_key=True)
    DE_LGL_ORGN_TYP = models.CharField(
        "LeganOrganizationTypeDescription", max_length=255)
    status = models.CharField(
        max_length=100,
        choices=STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="Legal Organization type status (Active/Inactive)",
    )
    createdby = models.IntegerField(null=True, help_text="Created By")
    createddate = models.DateTimeField(
        null=True, blank=True, auto_now_add=True, help_text="Date Created"
    )
    updatedby = models.IntegerField(null=True, help_text="Updated By ")
    updateddate = models.DateTimeField(
        null=True, blank=True, auto_now=True, help_text="Last Updated Date"
    )

    class Meta:
        db_table = 'LU_LGL_ORGN'

    def __unicode__(self):
        return self.DE_LGL_ORGN_TYP


class Organization(models.Model):
    ID_ORGN = models.BigAutoField("OrganizationID", primary_key=True)
    ID_PRTY = models.ForeignKey(
        Party, on_delete=models.CASCADE, verbose_name="Party ID", db_column="ID_PRTY")
    # CD_LGL_STS = models.ForeignKey(LegalStatusType, on_delete=models.CASCADE,verbose_name="LegalStatusCode",db_column="CD_LGL_STS")  # NOSONAR
    NM_LGL = models.CharField("LegalName", max_length=40)
    NM_TRD = models.CharField("TradeName", max_length=40)
    DC_TRMN = models.DateTimeField("TerminationDate")
    NM_JRDT_OF_INCRP = models.CharField(
        "JurisdictionOfIncorporation", max_length=255)
    DC_INCRP = models.DateTimeField("IncorporationDate")
    # CD_LGL_ORGN_TYP = models.ForeignKey(LegalOrganizationsType, on_delete=models.CASCADE,
    #                                     verbose_name="LegalOrganizationTypeCode", db_column="CD_LGL_ORGN_TYP")
    DC_FSC_YR_END = models.DateTimeField("FiscalYearEndDate")
    # CD_BSN_ACTV = models.ForeignKey(BusinessActivityReference, on_delete=models.CASCADE,verbose_name="BusinessActivityCode",db_column="CD_BSN_ACTV")  # NOSONAR
    MO_LCL_ANN_RVN = models.DecimalField(
        "LocalAnnualRevenueAmount", max_digits=16, decimal_places=5)
    MO_GBL_ANN_RVN = models.DecimalField(
        "GlobalAnnualRevenueAmount", max_digits=16, decimal_places=5)
    DC_OPN_FR_BSN = models.DateTimeField("OpenForBusinessDate")
    DC_CLSD_FR_BSN = models.DateTimeField("ClosedForBusinessDate")
    ID_DUNS_NBR = models.CharField("DUNSNumber", max_length=9, unique=True)
    FL_BNKRPTY = models.BooleanField('BankruptcyFlag', default=False)
    DC_BNKRPTY = models.DateTimeField("BankruptcyDate")
    DC_BNKRPTY_EMRGNC = models.DateTimeField("BankruptcyEmergenceDate")
    CD_BNKRPTY_TYP = models.CharField("BankruptcyTypeCode", max_length=20)
    QU_EM_CNT_LCL = models.IntegerField("EmployeeCountLocal")
    QU_EM_CNT_GBL = models.IntegerField("EmployeeCountGlobal")
    CD_RTG_DUNN_AND_BRDST = models.CharField(
        "DunnAndBradstreetRating", max_length=20)
    ID_LGE_PRMRY = models.ForeignKey(Language, on_delete=models.CASCADE,
                                     verbose_name="PrimaryBusinessLanguage", db_column="ID_LGE_PRMRY")
    NA_DE_ORGN = models.TextField("OrganizationDescriptionNarrative")
    # CD_GBL_BSN_TYP
    # NM_RLGN
    # CD_RLGN_FMY

    class Meta:
        db_table = 'PA_ORGN'

    def __unicode__(self):
        return self.ID_ORGN


class PartyIdentificationType(models.Model):
    TY_PRTY_ID = models.CharField(
        "PartyIdentificationTypeCode", max_length=2, primary_key=True)
    DE_PRTY_ID = models.CharField("Description", max_length=255)

    class Meta:
        db_table = 'PA_TYP_IDTN'

    def __unicode__(self):
        return self.TY_PRTY_ID


class ExternalPartyIdentificationProvider(models.Model):
    ID_PA_PVR_EXTRN = models.BigAutoField(
        "ExternalPartyIdentificationProviderID", primary_key=True)
    ID_PRTY_RO_ASGMT = models.ForeignKey(
        PartyRoleAssignment, on_delete=models.CASCADE, verbose_name="PartyRoleAssignmentID", db_column="ID_PRTY_RO_ASGMT")

    class Meta:
        db_table = 'PA_PVR_EXTRN_IDTN'

    def __unicode__(self):
        return self.ID_PA_PVR_EXTRN


class PartyIdentification(models.Model):
    ID_PA_IDTN = models.BigAutoField("PartyIdentificationID", primary_key=True)
    ID_PRTY = models.ForeignKey(
        Party, on_delete=models.CASCADE, verbose_name="Party ID", db_column="ID_PRTY")
    TY_PRTY_ID = models.ForeignKey(
        PartyIdentificationType, on_delete=models.CASCADE, verbose_name="Party ID", db_column="TY_PRTY_ID")
    DT_EF = models.DateTimeField("EffectiveDate")
    ID_PRTY_PRS = models.ForeignKey(
        Person, on_delete=models.CASCADE, verbose_name="PersonPartyID", db_column="ID_PRTY_PRS")
    ID_ADS = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name="AddressID", db_column="ID_ADS")
    ID_PA_PVR_EXTRN = models.ForeignKey(ExternalPartyIdentificationProvider, on_delete=models.CASCADE,
                                        verbose_name="ExternalPartyIdentificationProviderID", db_column="ID_PA_PVR_EXTRN")
    LU_ID_PRTY = models.IntegerField("Identifier", unique=True)
    DC_ISS = models.DateTimeField("IssueDate")
    DC_ID_PRTY_EP = models.DateTimeField("ExpirationDate")

    class Meta:
        db_table = 'PA_IDTN'

    def __unicode__(self):
        return self.ID_PA_IDTN
