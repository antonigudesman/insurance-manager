from __future__ import unicode_literals

from django.db import models
import uuid

INDUSTRY_CHOICES = (
    (None, 'NULL'),
    ('Accommodation & Food Services - All', 'Accommodation & Food Services - All'),
    ('Agriculture, Forestry, Fishing & Hunting - All', 'Agriculture, Forestry, Fishing & Hunting - All'),
    ('Arts, Entertainment, & Recreation - All', 'Arts, Entertainment, & Recreation - All'),
    ('Construction - All', 'Construction - All'),
    ('Educational Services - Colleges & Universities', 'Educational Services - Colleges & Universities'),
    ('Educational Services - Miscellaneous', 'Educational Services - Miscellaneous'),
    ('Educational Services - Primary & Secondary Schools', 'Educational Services - Primary & Secondary Schools'),
    ('Finance & Insurance - Banking', 'Finance & Insurance - Banking'),
    ('Finance & Insurance - Insurance Agents & Services', 'Finance & Insurance - Insurance Agents & Services'),
    ('Finance & Insurance - Insurance Carriers', 'Finance & Insurance - Insurance Carriers'),
    ('Finance & Insurance - Investment Services', 'Finance & Insurance - Investment Services'),
    ('Healthcare & Welfare - Child Day Care Services', 'Healthcare & Welfare - Child Day Care Services'),
    ('Healthcare & Welfare - Diagnostic Laboratories', 'Healthcare & Welfare - Diagnostic Laboratories'),
    ('Healthcare & Welfare - Home Healthcare Services', 'Healthcare & Welfare - Home Healthcare Services'),
    ('Healthcare & Welfare - Hospitals', 'Healthcare & Welfare - Hospitals'),
    ('Healthcare & Welfare - Nursing & Residential Care', 'Healthcare & Welfare - Nursing & Residential Care'),
    ('Healthcare & Welfare - Outpatient Care', 'Healthcare & Welfare - Outpatient Care'),
    ('Healthcare & Welfare - Physicians & Practitioners', 'Healthcare & Welfare - Physicians & Practitioners'),
    ('Healthcare & Welfare - Social Services', 'Healthcare & Welfare - Social Services'),
    ('Holding Companies - All', 'Holding Companies - All'),
    ('Information - Media & Broadcasting', 'Information - Media & Broadcasting'),
    ('Information - Miscellaneous', 'Information - Miscellaneous'),
    ('Information - Printing & Publishing', 'Information - Printing & Publishing'),
    ('Information - Software & Data Processing', 'Information - Software & Data Processing'),
    ('Information - Telecommunications', 'Information - Telecommunications'),
    ('Manufacturing - Apparel & Textiles', 'Manufacturing - Apparel & Textiles'),
    ('Manufacturing - Chemicals', 'Manufacturing - Chemicals'),
    ('Manufacturing - Consumer Goods', 'Manufacturing - Consumer Goods'),
    ('Manufacturing - Electronic Components', 'Manufacturing - Electronic Components'),
    ('Manufacturing - Food', 'Manufacturing - Food'),
    ('Manufacturing - Machinery & Equipment', 'Manufacturing - Machinery & Equipment'),
    ('Manufacturing - Medical Instruments & Supplies', 'Manufacturing - Medical Instruments & Supplies'),
    ('Manufacturing - Metal Products', 'Manufacturing - Metal Products'),
    ('Manufacturing - Pharmaceutical', 'Manufacturing - Pharmaceutical'),
    ('Manufacturing - Transportation & Aerospace', 'Manufacturing - Transportation & Aerospace'),
    ('Mining, Oil, & Gas Extraction - All', 'Mining, Oil, & Gas Extraction - All'),
    ('Public Administration - Courts & Public Safety', 'Public Administration - Courts & Public Safety'),
    ('Public Administration - Miscellaneous', 'Public Administration - Miscellaneous'),
    ('Public Administration - Municipalities', 'Public Administration - Municipalities'),
    ('Real Estate & Leasing - Non-Real Estate Leasing', 'Real Estate & Leasing - Non-Real Estate Leasing'),
    ('Real Estate & Leasing - Real Estate Agents', 'Real Estate & Leasing - Real Estate Agents'),
    ('Real Estate & Leasing - Real Estate Management', 'Real Estate & Leasing - Real Estate Management'),
    ('Retail - Department, Apparel, & Sporting Goods', 'Retail - Department, Apparel, & Sporting Goods'),
    ('Retail - Grocery, Liquor & Personal Care', 'Retail - Grocery, Liquor & Personal Care'),
    ('Retail - Home Furnishings, Appliances & Garden', 'Retail - Home Furnishings, Appliances & Garden'),
    ('Retail - Motor Vehicle & Parts Dealers', 'Retail - Motor Vehicle & Parts Dealers'),
    ('Services - Accounting & Tax', 'Services - Accounting & Tax'),
    ('Services - Advertising & Market Research', 'Services - Advertising & Market Research'),
    ('Services - Architecture & Engineering', 'Services - Architecture & Engineering'),
    ('Services - Associations & Organizations', 'Services - Associations & Organizations'),
    ('Services - Business Support Services', 'Services - Business Support Services'),
    ('Services - Computer System Design Services', 'Services - Computer System Design Services'),
    ('Services - Consulting Services', 'Services - Consulting Services'),
    ('Services - Employment Services', 'Services - Employment Services'),
    ('Services - Investigation & Security Services', 'Services - Investigation & Security Services'),
    ('Services - Legal Services', 'Services - Legal Services'),
    ('Services - Machinery Repair & Maintenance', 'Services - Machinery Repair & Maintenance'),
    ('Services - Research & Development Services', 'Services - Research & Development Services'),
    ('Transportation & Warehousing - All', 'Transportation & Warehousing - All'),
    ('Utilities - All', 'Utilities - All'),
    ('Waste Management & Remediation - All', 'Waste Management & Remediation - All'),
    ('Wholesale - All', 'Wholesale - All')
)

STATE_CHOICES = (
    (None, 'NULL'),
    ('Alabama', 'Alabama'),
    ('Alaska', 'Alaska'),
    ('Arizona', 'Arizona'),
    ('Arkansas', 'Arkansas'),
    ('California', 'California'),
    ('Colorado', 'Colorado'),
    ('Connecticut', 'Connecticut'),
    ('Delaware', 'Delaware'),
    ('District of Columbia', 'District of Columbia'),
    ('Florida', 'Florida'),
    ('Georgia', 'Georgia'),
    ('Hawaii', 'Hawaii'),
    ('Idaho', 'Idaho'),
    ('Illinois', 'Illinois'),
    ('Indiana', 'Indiana'),
    ('Iowa', 'Iowa'),
    ('Kansas', 'Kansas'),
    ('Kentucky', 'Kentucky'),
    ('Louisiana', 'Louisiana'),
    ('Maine', 'Maine'),
    ('Maryland', 'Maryland'),
    ('Massachusetts', 'Massachusetts'),
    ('Michigan', 'Michigan'),
    ('Minnesota', 'Minnesota'),
    ('Mississippi', 'Mississippi'),
    ('Missouri', 'Missouri'),
    ('Montana', 'Montana'),
    ('Nebraska', 'Nebraska'),
    ('Nevada', 'Nevada'),
    ('New Hampshire', 'New Hampshire'),
    ('New Jersey', 'New Jersey'),
    ('New Mexico', 'New Mexico'),
    ('New York', 'New York'),
    ('North Carolina', 'North Carolina'),
    ('North Dakota', 'North Dakota'),
    ('Ohio', 'Ohio'),
    ('Oklahoma', 'Oklahoma'),
    ('Oregon', 'Oregon'),
    ('Pennsylvania', 'Pennsylvania'),
    ('Rhode Island', 'Rhode Island'),
    ('South Carolina', 'South Carolina'),
    ('South Dakota', 'South Dakota'),
    ('Tennessee', 'Tennessee'),
    ('Texas', 'Texas'),
    ('Utah', 'Utah'),
    ('Vermont', 'Vermont'),
    ('Virginia', 'Virginia'),
    ('Washington', 'Washington'),
    ('West Virginia', 'West Virginia'),    
    ('Wisconsin', 'Wisconsin'),
    ('Wyoming', 'Wyoming')
)

class Employer(models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    name = models.CharField('Name',max_length=100)
    broker = models.CharField('Broker',max_length=75, null=True, blank=True) 
    industry1 = models.CharField('Industry 1',max_length=75, null=True, blank=True, choices=INDUSTRY_CHOICES)
    industry2 = models.CharField('Industry 2',max_length=75, null=True, blank=True, choices=INDUSTRY_CHOICES) 
    industry3 = models.CharField('Industry 3',max_length=75, null=True, blank=True, choices=INDUSTRY_CHOICES) 
    state = models.CharField('State',max_length=25, null=True, blank=True, choices=STATE_CHOICES)
    size = models.IntegerField('Size',blank=True, null=True)
    nonprofit = models.BooleanField('Non-Profit')
    govt_contractor = models.BooleanField('Govt Contractors')
    new_england = models.BooleanField('New England Region')
    mid_atlantic = models.BooleanField('Mid Atlantic Region')
    south_atlantic = models.BooleanField('South Atlantic Region')
    south_cental = models.BooleanField('South Central Region')
    east_central = models.BooleanField('East Central Region')
    west_central = models.BooleanField('West Central Region')
    mountain = models.BooleanField('Mountain Region')
    pacific = models.BooleanField('Pacific Region')
    med_count = models.IntegerField('Medical',default=0) 
    den_count = models.IntegerField('Dental',default=0) 
    vis_count = models.IntegerField('Vision',default=0) 
    life_count = models.IntegerField('Life',default=0) 
    std_count = models.IntegerField('STD',default=0) 
    ltd_count = models.IntegerField('LTD',default=0) 

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.id = str(uuid.uuid4())[:18]
            super(ScrapyTask, self).save(*args, **kwargs)


MED_TYPE_CHOICES = (
    ('PPO', 'PPO'),
    ('POS', 'POS'),
    ('HMO', 'HMO'),
    ('EPO', 'EPO'),
    ('HDHP', 'HDHP')
)

MED_BOOL_CHOICES = (
    (None, 'NULL'),
    ('FALSE', 'False'),
    ('False/Coin', 'False/Coin'),
    ('TRUE', 'True'),
    ('True/Coin', 'True/Coin')
)

class Medical(models.Model):
    title = models.CharField('Title',max_length=20)
    employer = models.ForeignKey(Employer)
    type = models.  CharField('Type',max_length=4, choices=MED_TYPE_CHOICES)
    in_ded_single = models.IntegerField('IN Deductible (Ind)', blank=True, null=True)
    in_max_single = models.IntegerField('IN Deductible (Fam)', blank=True, null=True)
    in_ded_family = models.IntegerField('IN Maximum (Ind)',blank=True, null=True)
    in_max_family = models.IntegerField('IN Maximum (Fam)',blank=True, null=True)
    in_coin = models.IntegerField('IN Coinsurance', blank=True, null=True)
    out_ded_single = models.IntegerField('OON Deductible (Ind)',blank=True, null=True)
    out_ded_family = models.IntegerField('OON Deductible (Fam)',blank=True, null=True)
    out_max_single = models.IntegerField('OON Maximum (Ind)',blank=True, null=True)
    out_max_family = models.IntegerField('OON Maximum (Fam)',blank=True, null=True)
    out_coin = models.IntegerField('OON Coinsurance',blank=True, null=True)
    rx_ded_single = models.IntegerField('Rx Deductible (Ind)',blank=True, null=True)
    rx_ded_family = models.IntegerField('Rx Deductible (Fam)',blank=True, null=True)
    rx_max_single = models.IntegerField('Rx Maximum (Ind)',blank=True, null=True)
    rx_max_family = models.IntegerField('Rx Maximum (Fam)',blank=True, null=True)
    rx_coin = models.IntegerField('Rx Coinsurance',blank=True, null=True)
    pcp_copay = models.IntegerField('PCP Copay',blank=True, null=True)
    sp_copay = models.IntegerField('Specialist Copay',blank=True, null=True)
    er_copay = models.IntegerField('ER Copay',blank=True, null=True)
    uc_copay = models.IntegerField('Urgent Care Copay',blank=True, null=True)
    lx_copay = models.IntegerField('Lab & Xray Copay',blank=True, null=True)
    ip_copay = models.IntegerField('Inpatient Copay',blank=True, null=True)
    op_copay = models.IntegerField('Outpatient Copay',blank=True, null=True)
    rx1_copay = models.IntegerField('Rx Tier 1 Copay',blank=True, null=True)
    rx2_copay = models.IntegerField('Rx Tier 2 Copay',blank=True, null=True)
    rx3_copay = models.IntegerField('Rx Tier 3 Copay',blank=True, null=True)
    rx4_copay = models.IntegerField('Rx Tier 4 Copay',blank=True, null=True)
    rx1_mail_copay = models.IntegerField('Rx Mail Tier 1 Copay',blank=True, null=True)
    rx2_mail_copay = models.IntegerField('Rx Mail Tier 2 Copay',blank=True, null=True)
    rx3_mail_copay = models.IntegerField('Rx Mail Tier 3 Copay',blank=True, null=True)
    rx4_mail_copay = models.IntegerField('Rx Mail Tier 4 Copay',blank=True, null=True)
    pcp_ded_apply = models.CharField('PCP Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    sp_ded_apply = models.CharField('Specialist Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    er_ded_apply = models.CharField('ER Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    uc_ded_apply = models.CharField('Urgent Care Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    lx_ded_apply = models.CharField('Lab & Xray Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    ip_ded_apply = models.CharField('Inpatient Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    op_ded_apply = models.CharField('Outpatient Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx1_ded_apply = models.CharField('Rx Tier 1 Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx2_ded_apply = models.CharField('Rx Tier 2 Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx3_ded_apply = models.CharField('Rx Tier 3 Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx4_ded_apply = models.CharField('Rx Tier 4 Ded Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    age_rated = models.NullBooleanField('Age Banded Rates')
    hra = models.NullBooleanField('Offer HRA')
    hsa = models.NullBooleanField('Offer HSA')
    ded_cross = models.NullBooleanField('Ded Cross Accumulate')
    max_cross = models.NullBooleanField('Max Cross Accumulate')
    t1_ee = models.IntegerField('Single Employee Cost',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse Employee Cost',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren) Employee Cost',blank=True, null=True)
    t4_ee = models.IntegerField('Family Employee Cost',blank=True, null=True)
    t1_gross = models.IntegerField('Single Gross Cost',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse Gross Cost',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren) Gross Cost',blank=True, null=True)
    t4_gross = models.IntegerField('Family Gross Cost',blank=True, null=True)
    t1_ercdhp = models.IntegerField('Single CDHP Funding',blank=True, null=True)
    t2_ercdhp = models.IntegerField('EE & Spouse CDHP Funding',blank=True, null=True)
    t3_ercdhp = models.IntegerField('EE & Child(ren) CDHP Funding',blank=True, null=True)
    t4_ercdhp = models.IntegerField('Family CDHP Funding',blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Medical Plan'
        verbose_name_plural = 'Medical Plans'
    

DEN_TYPE_CHOICES = (
    ('DPPO', 'DPPO'),
    ('DMO', 'DMO'),
)

class Dental(models.Model):
    title = models.CharField('Title', max_length=20)
    employer = models.ForeignKey(Employer)
    type = models.CharField('Type', max_length=4, choices=DEN_TYPE_CHOICES)
    in_ded_single = models.IntegerField('IN Deductible (Ind)', blank=True, null=True)
    in_ded_family = models.IntegerField('IN Deductible (Fam)', blank=True, null=True)
    in_max = models.IntegerField('IN Maximum (PP)', blank=True, null=True)
    in_max_ortho = models.IntegerField('IN Ortho Max (PP)', blank=True, null=True)
    out_ded_single = models.IntegerField('OON Deductible (Ind)', blank=True, null=True)
    out_ded_family = models.IntegerField('OON Deductible (Fam)', blank=True, null=True)
    out_max = models.IntegerField('OON Maximum (PP)', blank=True, null=True)
    out_max_ortho = models.IntegerField('OON Ortho Max (PP)', blank=True, null=True)
    in_prev_coin = models.IntegerField('IN Preventive', blank=True, null=True)
    out_prev_coin = models.IntegerField('OON Preventive', blank=True, null=True)
    prev_ded_apply = models.NullBooleanField('Preventive Ded Applies')
    in_basic_coin = models.IntegerField('IN Basic', blank=True, null=True)
    out_basic_coin = models.IntegerField('OON Basic', blank=True, null=True)
    basic_ded_apply = models.NullBooleanField('Basic Ded Applies')
    in_major_coin = models.IntegerField('IN Major', blank=True, null=True)
    out_major_coin = models.IntegerField('OON Major', blank=True, null=True)
    major_ded_apply = models.NullBooleanField('Major Ded Applies')
    in_ortho_coin = models.IntegerField('IN Ortho', blank=True, null=True)
    out_ortho_coin = models.IntegerField('OON Ortho', blank=True, null=True)
    ortho_ded_apply = models.NullBooleanField('Ortho Ded Applies')
    ortho_age_limit = models.IntegerField('Ortho Age Limit', blank=True, null=True)
    t1_ee = models.IntegerField('Single Employee Cost',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse Employee Cost',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren) Employee Cost',blank=True, null=True)
    t4_ee = models.IntegerField('Family Employee Cost',blank=True, null=True)
    t1_gross = models.IntegerField('Single Gross Cost',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse Gross Cost',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren) Gross Cost',blank=True, null=True)
    t4_gross = models.IntegerField('Family Gross Cost',blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Dental Plan'
        verbose_name_plural = 'Dental Plans'
    

class Vision(models.Model):
    title = models.CharField('Title', max_length=20)
    employer = models.ForeignKey(Employer)
    exam_copay = models.IntegerField('Exam Copay', blank=True, null=True)
    exam_frequency = models.IntegerField('Exam Frequency', blank=True, null=True)
    exam_out_allowance = models.IntegerField('Exam OON Allowance', blank=True, null=True)
    lenses_copay = models.IntegerField('Lenses Copay', blank=True, null=True)
    lenses_frequency = models.IntegerField('Lenses Frequency', blank=True, null=True)
    lenses_out_allowance = models.IntegerField('Lenses OON Allowance', blank=True, null=True)
    frames_copay = models.IntegerField('Frames Copay', blank=True, null=True)
    frames_allowance = models.IntegerField('Frames Allowance', blank=True, null=True)
    frames_coinsurance = models.IntegerField('Frames Coinsurance', blank=True, null=True)
    frames_frequency = models.IntegerField('Frames Frequency', blank=True, null=True)
    frames_out_allowance = models.IntegerField('Frames OON Allowance', blank=True, null=True)
    contacts_copay = models.IntegerField('Contacts Copay', blank=True, null=True)
    contacts_allowance = models.IntegerField('Contacts Allowance', blank=True, null=True)
    contacts_coinsurance = models.IntegerField('Contacts Coinsurance', blank=True, null=True)
    contacts_frequency = models.IntegerField('Contacts Frequency', blank=True, null=True)
    contacts_out_allowance = models.IntegerField('Contacts OON Allowance', blank=True, null=True)
    t1_ee = models.IntegerField('Single Employee Cost',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse Employee Cost',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren) Employee Cost',blank=True, null=True)
    t4_ee = models.IntegerField('Family Employee Cost',blank=True, null=True)
    t1_gross = models.IntegerField('Single Gross Cost',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse Gross Cost',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren) Gross Cost',blank=True, null=True)
    t4_gross = models.IntegerField('Family Gross Cost',blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Vision Plan'
        verbose_name_plural = 'Vision Plans'
    

LIFE_TYPE_CHOICES = (
    ('Multiple of Salary', 'Multiple of Salary'),
    ('Flat Amount', 'Flat Amount')
)        

COSTSHARE_CHOICES = (
    ('100% Employer Paid', '100% Employer Paid'),
    ('Employee Cost Share', 'Employee Cost Share')
)


class Life(models.Model):
    title = models.CharField('Title', max_length=20)
    employer = models.ForeignKey(Employer)
    type = models.CharField('Type', max_length=18, choices=LIFE_TYPE_CHOICES)
    multiple = models.FloatField('Multiple', blank=True, null=True)
    multiple_max = models.IntegerField('Multiple Max', blank=True, null=True)
    flat_amount = models.IntegerField('Flat Amount', blank=True, null=True)
    add = models.BooleanField('ADD')
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Life Plan'
        verbose_name_plural = 'Life Plans'
    

class STD(models.Model):
    title = models.CharField('Title', max_length=20)
    employer = models.ForeignKey(Employer)
    salary_cont = models.BooleanField('Salary Continuation')
    waiting_days = models.IntegerField('Waiting Days (Injury)', blank=True, null=True)
    waiting_days_sick = models.IntegerField('Waiting Days (Sick)', blank=True, null=True)
    duration_weeks = models.IntegerField('Duration Weeks', blank=True, null=True)
    percentage = models.IntegerField('Percentage', blank=True, null=True)
    weekly_max = models.IntegerField('Weekly Max', blank=True, null=True)
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'STD Plan'
        verbose_name_plural = 'STD Plans'


class LTD(models.Model):
    title = models.CharField('Title', max_length=20)
    employer = models.ForeignKey(Employer)
    waiting_weeks = models.IntegerField('Waiting Weeks', blank=True, null=True)
    percentage = models.IntegerField('Percentage', blank=True, null=True)
    monthly_max = models.IntegerField('Monthly Max', blank=True, null=True)
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'LTD Plan'
        verbose_name_plural = 'LTD Plans'
        

CB_CHOICES = (
    (None, 'NULL'),
    ('Med + Den', 'Med + Den'),
    ('Med + Vision', 'Med + Vision'),
    ('Med + Den + Vision', 'Med + Den + Vision'),
    ('Den + Vision', 'Den + Vision')
)

class Strategy(models.Model):
    employer = models.ForeignKey(Employer)
    offer_vol_life = models.NullBooleanField('Offer Voluntary Life')
    offer_vol_std = models.NullBooleanField('Offer Voluntary STD')
    offer_vol_ltd = models.NullBooleanField('Offer Voluntary LTD')
    spousal_surcharge = models.NullBooleanField('Require Spousal Surcharge')
    spousal_surcharge_amount = models.IntegerField('Spousal Surcharge Amount', blank=True, null=True)
    tobacco_surcharge = models.NullBooleanField('Require Tobacco Surcharge')
    tobacco_surcharge_amount = models.IntegerField('Tobacco Surcharge Amount', blank=True, null=True)
    defined_contribution = models.NullBooleanField('Defined Contribution')
    offer_fsa = models.NullBooleanField('Offer FSA')
    pt_medical = models.NullBooleanField('Part-Time Medical')
    pt_dental = models.NullBooleanField('Part-Time Dental')
    pt_vision = models.NullBooleanField('Part-Time Vision')
    pt_life = models.NullBooleanField('Part-Time Life')
    pt_std = models.NullBooleanField('Part-Time STD')
    pt_ltd = models.NullBooleanField('Part-Time LTD')
    salary_banding = models.NullBooleanField('Salary Banding')
    wellness_banding = models.NullBooleanField('Wellness Banding')
    narrow_network = models.NullBooleanField('Narrow Network')
    mec = models.NullBooleanField('Offer MEC Plan')
    mvp = models.NullBooleanField('Offer MVP Plan')    
    contribution_bundle = models.CharField('Contribution Bundling', max_length=19, null=True, blank=True, choices=CB_CHOICES)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Employer Strategy'
        verbose_name_plural = 'Employer Strategies'

