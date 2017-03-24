from __future__ import unicode_literals

from django.db import models


class Employer(models.Model):
    id = models.CharField(max_length=18, primary_key=True)
    name = models.CharField(max_length=100)
    broker = models.CharField(max_length=75, null=True, blank=True) 
    industry1 = models.CharField(max_length=75, null=True, blank=True)
    industry2 = models.CharField(max_length=75, null=True, blank=True) 
    industry3 = models.CharField(max_length=75, null=True, blank=True) 
    state = models.CharField(max_length=25, null=True, blank=True)
    size = models.IntegerField(blank=True, null=True)
    nonprofit = models.BooleanField()
    govt_contractor = models.BooleanField()
    new_england = models.BooleanField()
    mid_atlantic = models.BooleanField()
    south_atlantic = models.BooleanField()
    south_cental = models.BooleanField()
    east_central = models.BooleanField()
    west_central = models.BooleanField()
    mountain = models.BooleanField()
    pacific = models.BooleanField()
    med_count = models.IntegerField(default=0) 
    den_count = models.IntegerField(default=0) 
    vis_count = models.IntegerField(default=0) 
    life_count = models.IntegerField(default=0) 
    std_count = models.IntegerField(default=0) 
    ltd_count = models.IntegerField(default=0) 

    def __unicode__(self):
        return self.name


class Vision(models.Model):
    title = models.CharField(max_length=20)
    employer = models.ForeignKey(Employer)
    exam_copay = models.IntegerField(blank=True, null=True)
    exam_frequency = models.IntegerField(blank=True, null=True)
    exam_out_allowance = models.IntegerField(blank=True, null=True)
    lenses_copay = models.IntegerField(blank=True, null=True)
    lenses_frequency = models.IntegerField(blank=True, null=True)
    lenses_out_allowance = models.IntegerField(blank=True, null=True)
    frames_copay = models.IntegerField(blank=True, null=True)
    frames_allowance = models.IntegerField(blank=True, null=True)
    frames_coinsurance = models.IntegerField(blank=True, null=True)
    frames_frequency = models.IntegerField(blank=True, null=True)
    frames_out_allowance = models.IntegerField(blank=True, null=True)
    contacts_copay = models.IntegerField(blank=True, null=True)
    contacts_allowance = models.IntegerField(blank=True, null=True)
    contacts_coinsurance = models.IntegerField(blank=True, null=True)
    contacts_frequency = models.IntegerField(blank=True, null=True)
    contacts_out_allowance = models.IntegerField(blank=True, null=True)
    t1_ee = models.IntegerField(blank=True, null=True)
    t2_ee = models.IntegerField(blank=True, null=True)
    t3_ee = models.IntegerField(blank=True, null=True)
    t4_ee = models.IntegerField(blank=True, null=True)
    t1_gross = models.IntegerField(blank=True, null=True)
    t2_gross = models.IntegerField(blank=True, null=True)
    t3_gross = models.IntegerField(blank=True, null=True)
    t4_gross = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name_plural = 'Vision Plans'
    

class Life(models.Model):
    title = models.CharField(max_length=20)
    employer = models.ForeignKey(Employer)
    type = models.CharField(max_length=18)
    multiple = models.FloatField(blank=True, null=True)
    multiple_max = models.IntegerField(blank=True, null=True)
    flat_amount = models.IntegerField(blank=True, null=True)
    add = models.BooleanField()
    cost_share = models.CharField(max_length=19, null=True, blank=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name_plural = 'Life Plans'
    

class STD(models.Model):
    title = models.CharField(max_length=20)
    employer = models.ForeignKey(Employer)
    salary_cont = models.BooleanField()
    waiting_days = models.IntegerField(blank=True, null=True)
    waiting_days_sick = models.IntegerField(blank=True, null=True)
    duration_weeks = models.IntegerField(blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    weekly_max = models.IntegerField(blank=True, null=True)
    cost_share = models.CharField(max_length=19, null=True, blank=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name_plural = 'STD Plans'


class LTD(models.Model):
    title = models.CharField(max_length=20)
    employer = models.ForeignKey(Employer)
    waiting_weeks = models.IntegerField(blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    monthly_max = models.IntegerField(blank=True, null=True)
    cost_share = models.CharField(max_length=19, null=True, blank=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name_plural = 'LTD Plans'
        

class Strategy(models.Model):
    employer = models.ForeignKey(Employer)
    offer_vol_life = models.NullBooleanField()
    offer_vol_std = models.NullBooleanField()
    offer_vol_ltd = models.NullBooleanField()
    spousal_surcharge = models.NullBooleanField()
    spousal_surcharge_amount = models.IntegerField(blank=True, null=True)
    tobacco_surcharge = models.NullBooleanField()
    tobacco_surcharge_amount = models.IntegerField(blank=True, null=True)
    defined_contribution = models.NullBooleanField()
    offer_fsa = models.NullBooleanField()
    pt_medical = models.NullBooleanField()
    pt_dental = models.NullBooleanField()
    pt_vision = models.NullBooleanField()
    pt_life = models.NullBooleanField()
    pt_std = models.NullBooleanField()
    pt_ltd = models.NullBooleanField()
    salary_banding = models.NullBooleanField()
    wellness_banding = models.NullBooleanField()
    narrow_network = models.NullBooleanField()
    mec = models.NullBooleanField()
    mvp = models.NullBooleanField()    
    contribution_bundle = models.CharField(max_length=19, null=True, blank=True)

    def __unicode__(self):
        return self.employer.name
        
    class Meta:
        verbose_name_plural = 'Strategies'

