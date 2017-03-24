import csv
from django.http import HttpResponse
from .models import *


def import_employer(request):
    path = '/home/akimmel/work/table extracts/employers.csv'
    # path = '/root/work/Enterprise/data/employers.csv'
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                employer = Employer.objects.create(
                    id=row['ID'],
                    # name=row['NAME'].decode('utf8'),
                    name = unicode(row['NAME'], errors='ignore'),
                    broker=row['BROKER__C'],
                    industry1=row['INDUSTRY_1__C'],
                    industry2=row['INDUSTRY_2__C'],
                    industry3=row['INDUSTRY_3__C'],
                    state=row['EMPLOYERSTATE__C'],
                    size=row['EMPLOYERHEADCOUNT__C'],
                    nonprofit=row['NON_PROFIT__C']=='TRUE',
                    govt_contractor=row['GOVT_CONTRACTOR__C']=='TRUE',
                    med_count=row['MEDICAL_PLANS__C'],
                    den_count=row['DENTAL_PLANS__C'],
                    vis_count=row['VISION_PLANS__C'],
                    life_count=row['LIFE_PLANS__C'],
                    std_count=row['STD_PLANS__C'],
                    ltd_count=row['LTD_PLANS__C'],
                    new_england=row['DISTRICT_NEW_ENGLAND__C']=='TRUE',
                    mid_atlantic=row['DISTRICT_MID_ATLANTIC__C']=='TRUE',
                    south_atlantic=row['DISTRICT_SOUTH_ATLANTIC__C']=='TRUE',
                    south_cental=row['DISTRICT_SOUTH_CENTRAL__C']=='TRUE',
                    east_central=row['DISTRICT_EAST_NORTH_CENTRAL__C']=='TRUE',
                    west_central=row['DISTRICT_WEST_NORTH_CENTRAL__C']=='TRUE',
                    mountain=row['DISTRICT_MOUNTAIN__C']=='TRUE',
                    pacific=row['DISTRICT_PACIFIC__C']=='TRUE')
            except Exception as e:
                print str(e)
                print row['ID'], '#{}#'.format(row['EMPLOYERHEADCOUNT__C'])

    return HttpResponse('Successfully imported ({})!'.format(Employer.objects.all().count()))


def import_vision(request):
    path = '/home/akimmel/work/table extracts/vision.csv'
    # path = '/root/work/Enterprise/data/vision.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                vision = Vision.objects.create(          
                    title='Option V',
                    employer_id=row['EMPLOYERNAME__C'],
                    exam_copay=row['VP_EXAM_COPAY__C'] or None,
                    exam_frequency=row['VP_EXAM_FREQUENCY__C'] or None,
                    exam_out_allowance=row['VP_EXAM_OUT_ALLOWANCE__C'] or None,
                    lenses_copay=row['VP_LENSES_COPAY__C'] or None,
                    lenses_frequency=row['VP_LENSES_FREQUENCY__C'] or None,
                    lenses_out_allowance=row['VP_LENSES_OUT_ALLOWANCE__C'] or None,
                    frames_copay=row['VP_FRAMES_COPAY__C'] or None,
                    frames_allowance=row['VP_FRAMES_ALLOWANCE__C'] or None,
                    frames_coinsurance=row['VP_FRAMES_BALANCE_COINSURANCE__C'] or None,
                    frames_frequency=row['VP_FRAMES_FREQUENCY__C'] or None,
                    frames_out_allowance=row['VP_FRAMES_OUT_ALLOWANCE__C'] or None,
                    contacts_copay=row['VP_CONTACTS_COPAY__C'] or None,
                    contacts_allowance=row['VP_CONTACTS_ALLOWANCE__C'] or None,
                    contacts_coinsurance=row['VP_CONTACTS_BALANCE_COINSURANCE__C'] or None,
                    contacts_frequency=row['VP_CONTACTS_FREQUENCY__C'] or None,
                    contacts_out_allowance=row['VP_CONTACTS_OUT_ALLOWANCE__C'] or None,
                    t1_ee=row['VP_T1_ANNUAL_EE__C'] or None,
                    t2_ee=row['VP_T2_ANNUAL_EE__C'] or None,
                    t3_ee=row['VP_T3_ANNUAL_EE__C'] or None,
                    t4_ee=row['VP_T4_ANNUAL_EE__C'] or None,
                    t1_gross=row['VP_T1_ANNUAL_GROSS__C'] or None,
                    t2_gross=row['VP_T2_ANNUAL_GROSS__C'] or None,
                    t3_gross=row['VP_T3_ANNUAL_GROSS__C'] or None,
                    t4_gross=row['VP_T4_ANNUAL_GROSS__C'] or None)
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['EMPLOYERNAME__C'])
                # break

    return HttpResponse('Successfully imported ({})!'.format(Life.objects.all().count()))


def import_life(request):
    path = '/home/akimmel/work/table extracts/life.csv'
    # path = '/root/work/Enterprise/data/life.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                life = Life.objects.create(          
                    title='Option X',
                    employer_id=row['EMPLOYERNAME__C'],
                    type=row['LP_TYPE__C'],
                    multiple=row['LP_MULTIPLE__C'] or None,
                    multiple_max=row['LP_MULTIPLE_MAX__C'] or None,
                    flat_amount=row['LP_FLAT_AMOUNT__C'] or None,
                    add=row['LP_ADD__C']=='TRUE',
                    cost_share=row['LP_COST_SHARE__C'])
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['LP_MULTIPLE__C']), row['EMPLOYERNAME__C'], row['LP_TYPE__C']
                # break

    return HttpResponse('Successfully imported ({})!'.format(Life.objects.all().count()))


def import_std(request):
    path = '/home/akimmel/work/table extracts/STD.csv'    
    # path = '/root/work/Enterprise/data/STD.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                std = STD.objects.create(           
                    title='Option Y',
                    employer_id=row['EMPLOYER_NAME__C'],
                    salary_cont=row['STD_SALARY_CONTINUATION__C']=='TRUE',
                    waiting_days=row['STD_WAITING_DAYS__C'] or None,
                    waiting_days_sick=row['STD_WAITING_DAYS_SICK__C'] or None,
                    duration_weeks=row['STD_DURATION_WEEKS__C'] or None,
                    percentage=row['STD_PERCENTAGE__C'] or None,
                    weekly_max=row['STD_WEEKLY_MAX__C'] or None,
                    cost_share=row['STD_COST_SHARE__C'])
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['STD_COST_SHARE__C']), row['EMPLOYER_NAME__C']

    return HttpResponse('Successfully imported ({})!'.format(STD.objects.all().count()))


def import_ltd(request):
    path = '/home/akimmel/work/table extracts/LTD.csv'    
    # path = '/root/work/Enterprise/data/LTD.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                ltd = LTD.objects.create(               
                    title='Option Z',                                  
                    employer_id=row['EMPLOYERNAME__C'],
                    waiting_weeks=row['LTD_WAITING_WEEKS__C'] or None,
                    percentage=row['LTD_PERCENTAGE__C'] or None,
                    monthly_max=row['LTD_MONTHLY_MAX__C'] or None,
                    cost_share=row['LTD_COST_SHARE__C'])
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['LTD_COST_SHARE__C']), row['EMPLOYER_NAME__C']

    return HttpResponse('Successfully imported ({})!'.format(LTD.objects.all().count()))


def import_strategy(request):
    path = '/home/akimmel/work/table extracts/strategy.csv'    
    # path = '/root/work/Enterprise/data/strategy.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                strategy = Strategy.objects.create(  
                    employer_id=row['EMPLOYERNAME__C'],         
                    offer_vol_life=get_3_state_boolean(row['OFFER_VOLUNTARY_LIFE__C']),
                    offer_vol_std=get_3_state_boolean(row['OFFER_VOLUNTARY_STD__C']),
                    offer_vol_ltd=get_3_state_boolean(row['OFFER_VOLUNTARY_LTD__C']),
                    spousal_surcharge=get_3_state_boolean(row['SPOUSAL_SURCHARGE__C']),
                    spousal_surcharge_amount=row['SPOUSAL_SURCHARGE_ANNUAL_AMOUNT__C'] or None,
                    tobacco_surcharge=get_3_state_boolean(row['TOBACCO_SURCHARGE__C']),
                    tobacco_surcharge_amount=row['TOBACCO_SURCHARGE_ANNUAL_AMOUNT__C'] or None,
                    defined_contribution=get_3_state_boolean(row['DEFINED_CONTRIBUTION__C']),
                    offer_fsa=get_3_state_boolean(row['OFFER_FSA__C']),
                    pt_medical=get_3_state_boolean(row['OFFER_PART_TIME_MEDICAL__C']),
                    pt_dental=get_3_state_boolean(row['OFFER_PART_TIME_DENTAL__C']),
                    pt_vision=get_3_state_boolean(row['OFFER_PART_TIME_VISION__C']),
                    pt_life=get_3_state_boolean(row['OFFER_PART_TIME_LIFE__C']),
                    pt_std=get_3_state_boolean(row['OFFER_PART_TIME_STD__C']),
                    pt_ltd=get_3_state_boolean(row['OFFER_PART_TIME_LTD__C']),
                    salary_banding=get_3_state_boolean(row['SALARY_BANDING__C']),
                    wellness_banding=get_3_state_boolean(row['WELLNESS_BANDING__C']),
                    narrow_network=get_3_state_boolean(row['NARROW_NETWORK__C']),
                    mvp=get_3_state_boolean(row['MVP_PLAN__C']),
                    mec=get_3_state_boolean(row['MEC_PLAN__C']),
                    contribution_bundle=row['CONTRIBUTION_BUNDLING__C'])

            except Exception as e:
                print str(e)
                print row['EMPLOYERNAME__C']

    return HttpResponse('Successfully imported ({})!'.format(Strategy.objects.all().count()))


def get_3_state_boolean(value):
    if value == 'TRUE':
        return True
    elif value == 'FALSE':
        return False
