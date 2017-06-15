from __future__ import unicode_literals

import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User


STATE_CHOICES = (
    (None, '-'),
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


class Industry(models.Model):
    id = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'


class Broker(models.Model):
    id = models.CharField(max_length=150, primary_key=True)

    def __str__(self):
        return self.id


class Employer(models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    name = models.CharField('Name',max_length=100)
    broker = models.ForeignKey(Broker, verbose_name='Account')
    industry1 = models.ForeignKey(Industry, verbose_name='Primary Industry', null=True, blank=True, related_name="industry_1")
    industry2 = models.ForeignKey(Industry, verbose_name='Secondary Industry', null=True, blank=True, related_name="industry_2") 
    industry3 = models.ForeignKey(Industry, verbose_name='Additional Industry', null=True, blank=True, related_name="industry_3") 
    state = models.CharField('State',max_length=25, null=True, blank=True, choices=STATE_CHOICES)
    size = models.PositiveIntegerField('Size', validators=[MinValueValidator(1)])
    nonprofit = models.BooleanField('Non-Profit Organization')
    govt_contractor = models.BooleanField('Government Contractor')
    new_england = models.BooleanField('New England Region')
    mid_atlantic = models.BooleanField('Mid Atlantic Region')
    south_atlantic = models.BooleanField('South Atlantic Region')
    south_cental = models.BooleanField('South Central Region')
    east_central = models.BooleanField('East Central Region')
    west_central = models.BooleanField('West Central Region')
    mountain = models.BooleanField('Mountain Region')
    pacific = models.BooleanField('Pacific Region')
    med_count = models.IntegerField('Medical Plans',default=0) 
    den_count = models.IntegerField('Dental Plans',default=0) 
    vis_count = models.IntegerField('Vision Plans',default=0) 
    life_count = models.IntegerField('Life Plans',default=0) 
    std_count = models.IntegerField('STD Plans',default=0) 
    ltd_count = models.IntegerField('LTD Plans',default=0) 
    qc = models.BooleanField('QC', default=False)
    renewal_date = models.DateField('Renewal Date')
    address_line_1 = models.CharField('Address 1', max_length=50, blank=True, null=True)
    address_line_2 = models.CharField('Address 2', max_length=50, blank=True, null=True)
    zip_code = models.CharField('Zip Code', max_length=10, blank=True, null=True)
    phone = models.CharField('Phone', max_length=15, blank=True, null=True)
    country = models.CharField('Country', max_length=30, blank=True, null=True)
    naics_2012_code = models.IntegerField('NAICS', blank=True, null=True)
    avid = models.IntegerField('AVID', blank=True, null=True)
    employercity = models.CharField('City', max_length=50, blank=True, null=True)
    employerurl = models.CharField('URL', max_length=150, blank=True, null=True)
    employerbenefitsurl = models.CharField('Benefit URL', max_length=100, blank=True, null=True)
    stock_symbol = models.CharField('Stock Symbol', max_length=5, blank=True, null=True)

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = str(uuid.uuid4())[:18]
        super(Employer, self).save(*args, **kwargs)


MED_TYPE_CHOICES = (
    ('PPO', 'PPO'),
    ('POS', 'POS'),
    ('HMO', 'HMO'),
    ('EPO', 'EPO'),
    ('HDHP', 'HDHP')
)

MED_BOOL_CHOICES = (
    (None, '-'),
    ('FALSE', 'No Deductible'),
    ('False/Coin', 'No Deductible, then Coinsurance'),
    ('TRUE', 'Deductible'),
    ('True/Coin', 'Deductible, then Coinurance')
)


BOOLEAN_CHOICES =  (
    (None, '-'),
    (False, 'No Deductible'),
    (True, 'Deductible Applies')
)

class Medical(models.Model):
    title = models.CharField('Plan Name',max_length=30)
    employer = models.ForeignKey(Employer)
    type = models.CharField('Type',max_length=4, choices=MED_TYPE_CHOICES)
    in_ded_single = models.IntegerField('Individual Deductible', blank=True, null=True)
    in_ded_family = models.IntegerField('Family Deductible',blank=True, null=True)
    in_max_single = models.IntegerField('Individual Out-of-Pocket Maximum', blank=True, null=True)
    in_max_family = models.IntegerField('Family Out-of-Pocket Maximum',blank=True, null=True)
    in_coin = models.IntegerField('Coinsurance', blank=True, null=True)
    out_ded_single = models.IntegerField('Individual Deductible',blank=True, null=True)
    out_ded_family = models.IntegerField('Family Deductible',blank=True, null=True)
    out_max_single = models.IntegerField('Individual Out-of-Pocket Maximum',blank=True, null=True)
    out_max_family = models.IntegerField('Family Out-of-Pocket Maximum',blank=True, null=True)
    out_coin = models.IntegerField('Coinsurance',blank=True, null=True)
    rx_ded_single = models.IntegerField('Individual Deductible',blank=True, null=True)
    rx_ded_family = models.IntegerField('Family Deductible',blank=True, null=True)
    rx_max_single = models.IntegerField('Individual Out-of-Pocket Maximum',blank=True, null=True)
    rx_max_family = models.IntegerField('Family Out-of-Pocket Maximum',blank=True, null=True)
    rx_coin = models.IntegerField('Coinsurance',blank=True, null=True)
    pcp_copay = models.IntegerField('PCP Copay',blank=True, null=True)
    sp_copay = models.IntegerField('Specialist Copay',blank=True, null=True)
    er_copay = models.IntegerField('ER Copay',blank=True, null=True)
    uc_copay = models.IntegerField('Urgent Care Copay',blank=True, null=True)
    lx_copay = models.IntegerField('Lab & Xray Copay',blank=True, null=True)
    ip_copay = models.IntegerField('Inpatient Copay',blank=True, null=True)
    op_copay = models.IntegerField('Outpatient Copay',blank=True, null=True)
    rx1_copay = models.IntegerField('Tier 1 Retail (30) Copay',blank=True, null=True)
    rx2_copay = models.IntegerField('Tier 2 Retail (30) Copay',blank=True, null=True)
    rx3_copay = models.IntegerField('Tier 3 Retail (30) Copay',blank=True, null=True)
    rx4_copay = models.IntegerField('Tier 4 Retail (30) Copay',blank=True, null=True)
    rx1_mail_copay = models.IntegerField('Tier 1 Mail (90) Copay',blank=True, null=True)
    rx2_mail_copay = models.IntegerField('Tier 2 Mail (90) Copay',blank=True, null=True)
    rx3_mail_copay = models.IntegerField('Tier 3 Mail (90) Copay',blank=True, null=True)
    rx4_mail_copay = models.IntegerField('Tier 4 Mail (90) Copay',blank=True, null=True)
    pcp_ded_apply = models.CharField('PCP Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    sp_ded_apply = models.CharField('Specialist Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    er_ded_apply = models.CharField('ER Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    uc_ded_apply = models.CharField('Urgent Care Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    lx_ded_apply = models.CharField('Lab & Xray Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    ip_ded_apply = models.CharField('Inpatient Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    op_ded_apply = models.CharField('Outpatient Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx1_ded_apply = models.CharField('Tier 1 Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx2_ded_apply = models.CharField('Tier 2 Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx3_ded_apply = models.CharField('Tier 3 Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    rx4_ded_apply = models.CharField('Tier 4 Deductible Applies',max_length=20, blank=True, null=True, choices=MED_BOOL_CHOICES)
    age_rated = models.BooleanField('Age Banded Rates')
    hra = models.BooleanField('Offer HRA')
    hsa = models.BooleanField('Offer HSA')
    ded_cross = models.BooleanField('Ded Cross Accumulate')
    max_cross = models.BooleanField('Max Cross Accumulate')
    t1_ee = models.IntegerField('Single',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_ee = models.IntegerField('Family',blank=True, null=True)
    t1_gross = models.IntegerField('Single',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_gross = models.IntegerField('Family',blank=True, null=True)
    t1_ercdhp = models.IntegerField('Single',blank=True, null=True)
    t2_ercdhp = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_ercdhp = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_ercdhp = models.IntegerField('Family',blank=True, null=True)
    carrier = models.CharField('Carrier', max_length=30, blank=True, null=True)
    per_day_ip = models.NullBooleanField('Per Day IP', choices=BOOLEAN_CHOICES)

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
    title = models.CharField('Plan Name', max_length=30)
    employer = models.ForeignKey(Employer)
    type = models.CharField('Type', max_length=4, choices=DEN_TYPE_CHOICES)
    in_ded_single = models.IntegerField('Individual Deductible', blank=True, null=True)
    in_ded_family = models.IntegerField('Family Deductible', blank=True, null=True)
    in_max = models.IntegerField('Per Person Maximum', blank=True, null=True)
    in_max_ortho = models.IntegerField('Ortho Per Person Maximum', blank=True, null=True)
    out_ded_single = models.IntegerField('Individual Deductible', blank=True, null=True)
    out_ded_family = models.IntegerField('Family Deductible', blank=True, null=True)
    out_max = models.IntegerField('Per Person Maximum', blank=True, null=True)
    out_max_ortho = models.IntegerField('Per Person Ortho Maximum', blank=True, null=True)
    in_prev_coin = models.IntegerField('Preventive In-Network Coinsurance', blank=True, null=True)
    out_prev_coin = models.IntegerField('Preventive Out-of-Network Coinsurance', blank=True, null=True)
    prev_ded_apply = models.NullBooleanField('Preventive Deductible Applies', choices=BOOLEAN_CHOICES)
    in_basic_coin = models.IntegerField('Basic In-Network Coinsurance', blank=True, null=True)
    out_basic_coin = models.IntegerField('Basic Out-of-Network Coinsurance', blank=True, null=True)
    basic_ded_apply = models.NullBooleanField('Basic Deductible Applies', choices=BOOLEAN_CHOICES)
    in_major_coin = models.IntegerField('Major In-Network Coinsurance', blank=True, null=True)
    out_major_coin = models.IntegerField('Major Out-of-Network Coinsurance', blank=True, null=True)
    major_ded_apply = models.NullBooleanField('Major Deductible Applies', choices=BOOLEAN_CHOICES)
    in_ortho_coin = models.IntegerField('Ortho In-Network Coinsurance', blank=True, null=True)
    out_ortho_coin = models.IntegerField('Ortho Out-of-Network Coinsurance', blank=True, null=True)
    ortho_ded_apply = models.NullBooleanField('Ortho Deductible Applies', choices=BOOLEAN_CHOICES)
    ortho_age_limit = models.IntegerField('Ortho Age Limit', blank=True, null=True)
    t1_ee = models.IntegerField('Single',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_ee = models.IntegerField('Family',blank=True, null=True)
    t1_gross = models.IntegerField('Single',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_gross = models.IntegerField('Family',blank=True, null=True)
    carrier = models.CharField('Carrier', max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Dental Plan'
        verbose_name_plural = 'Dental Plans'
    

class Vision(models.Model):
    title = models.CharField('Plan Name', max_length=30)
    employer = models.ForeignKey(Employer)
    exam_copay = models.IntegerField('Exam Copay', blank=True, null=True)
    exam_frequency = models.IntegerField('Exam Frequency', blank=True, null=True)
    exam_out_allowance = models.IntegerField('Exam Allowance', blank=True, null=True)
    lenses_copay = models.IntegerField('Lenses Copay', blank=True, null=True)
    lenses_frequency = models.IntegerField('Lenses Frequency', blank=True, null=True)
    lenses_out_allowance = models.IntegerField('Lenses Allowance', blank=True, null=True)
    frames_copay = models.IntegerField('Frames Copay', blank=True, null=True)
    frames_allowance = models.IntegerField('Frames Allowance', blank=True, null=True)
    frames_coinsurance = models.IntegerField('Frames Coinsurance', blank=True, null=True)
    frames_frequency = models.IntegerField('Frames Frequency', blank=True, null=True)
    frames_out_allowance = models.IntegerField('Frames Allowance', blank=True, null=True)
    contacts_copay = models.IntegerField('Contacts Copay', blank=True, null=True)
    contacts_allowance = models.IntegerField('Contacts Allowance', blank=True, null=True)
    contacts_coinsurance = models.IntegerField('Contacts Coinsurance', blank=True, null=True)
    contacts_frequency = models.IntegerField('Contacts Frequency', blank=True, null=True)
    contacts_out_allowance = models.IntegerField('Contacts Allowance', blank=True, null=True)
    t1_ee = models.IntegerField('Single',blank=True, null=True)
    t2_ee = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_ee = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_ee = models.IntegerField('Family',blank=True, null=True)
    t1_gross = models.IntegerField('Single',blank=True, null=True)
    t2_gross = models.IntegerField('EE & Spouse',blank=True, null=True)
    t3_gross = models.IntegerField('EE & Child(ren)',blank=True, null=True)
    t4_gross = models.IntegerField('Family',blank=True, null=True)
    carrier = models.CharField('Carrier', max_length=30, blank=True, null=True)
    exam_allowance = models.IntegerField('Exam Allowance', blank=True, null=True)
    exam_balance_coinsurance = models.IntegerField('Exam Coinsurance', blank=True, null=True)
    lenses_allowance = models.IntegerField('Lenses Allowance',blank=True, null=True)
    lenses_balance_coinsurance = models.IntegerField('Lenses Coinsurance', blank=True, null=True)

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
    title = models.CharField('Plan Name', max_length=30)
    employer = models.ForeignKey(Employer)
    type = models.CharField('Type', max_length=18, choices=LIFE_TYPE_CHOICES)
    multiple = models.FloatField('Multiple Factor', blank=True, null=True)
    multiple_max = models.IntegerField('Multiple Maximum Amount', blank=True, null=True)
    flat_amount = models.IntegerField('Flat Amount', blank=True, null=True)
    add = models.BooleanField('ADD')
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)
    carrier = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'Life Plan'
        verbose_name_plural = 'Life Plans'
    

class STD(models.Model):
    title = models.CharField('Title', max_length=30)
    employer = models.ForeignKey(Employer)
    salary_cont = models.BooleanField('Salary Continuation')
    waiting_days = models.IntegerField('Waiting Days (Injury)', blank=True, null=True)
    waiting_days_sick = models.IntegerField('Waiting Days (Sick)', blank=True, null=True)
    duration_weeks = models.IntegerField('Duration Weeks', blank=True, null=True)
    percentage = models.IntegerField('Replacement Percentage', blank=True, null=True)
    weekly_max = models.IntegerField('Weekly Maximum', blank=True, null=True)
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)
    carrier = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'STD Plan'
        verbose_name_plural = 'STD Plans'


class LTD(models.Model):
    title = models.CharField('Title', max_length=30)
    employer = models.ForeignKey(Employer)
    waiting_weeks = models.IntegerField('Waiting Weeks', blank=True, null=True)
    percentage = models.IntegerField('Replacement Percentage', blank=True, null=True)
    monthly_max = models.IntegerField('Monthly Maximum', blank=True, null=True)
    cost_share = models.CharField('Cost Share', max_length=19, null=True, blank=True, choices=COSTSHARE_CHOICES)
    carrier = models.CharField(max_length=30, blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name = 'LTD Plan'
        verbose_name_plural = 'LTD Plans'
        

CB_CHOICES = (
    (None, '-'),
    ('Med + Den', 'Med + Den'),
    ('Med + Vision', 'Med + Vision'),
    ('Med + Den + Vision', 'Med + Den + Vision'),
    ('Den + Vision', 'Den + Vision')
)

STRATEGY_BOOLEAN_CHOICES =  (
    (None, '-'),
    (False, 'No'),
    (True, 'Yes')
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
    pt_medical = models.NullBooleanField('Offer Part-Time Medical')
    pt_dental = models.NullBooleanField('Offer Part-Time Dental')
    pt_vision = models.NullBooleanField('Offer Part-Time Vision')
    pt_life = models.NullBooleanField('Offer Part-Time Life')
    pt_std = models.NullBooleanField('Offer Part-Time STD')
    pt_ltd = models.NullBooleanField('Offer Part-Time LTD')
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


class FAQ(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    editor = models.ForeignKey(User, blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey('FAQCategory')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'


class FAQCategory(models.Model):
    title  = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'FAQ Category'
        verbose_name_plural = 'FAQ Categories'

class PrintHistory(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    benefit = models.CharField(max_length=50)
    plan = models.IntegerField(blank=True, null=True)
    plan_type = models.CharField(max_length=50, blank=True, null=True)
    ft_industries = models.TextField(blank=True, null=True)
    ft_head_counts = models.TextField(blank=True, null=True)
    ft_regions = models.TextField(blank=True, null=True)
    ft_states = models.TextField(blank=True, null=True)
    ft_other = models.TextField(blank=True, null=True)
    properties = models.TextField(blank=True, null=True)
    properties_inv = models.TextField(blank=True, null=True)
    services = models.TextField(blank=True, null=True)
    print_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Print History'
        verbose_name_plural = 'Print Histories'
            