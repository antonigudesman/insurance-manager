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
        