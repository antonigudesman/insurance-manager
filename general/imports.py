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


def import_medical(request):
    path = '/home/akimmel/work/table extracts/medical.csv'
    # path = '/root/work/Enterprise/data/medical.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                medical = Medical.objects.create(          
                    title='Option M',
                    employer_id=row['EMPLOYERNAME__C'],
                    type=row['MP_TYPE__C'] or None,
                    in_ded_single=row['MP_IN_DEDUCTIBLE_S__C'] or None,
                    in_ded_family=row['MP_IN_DEDUCTIBLE_F__C'] or None,
                    in_max_single=row['MP_IN_MAXIMUM_S__C'] or None,
                    in_max_family=row['MP_IN_MAXIMUM_F__C'] or None,
                    in_coin=row['MP_IN_COINSURANCE__C'] or None,
                    out_ded_single=row['MP_OUT_DEDUCTIBLE_S__C'] or None,
                    out_ded_family=row['MP_OUT_DEDUCTIBLE_F__C'] or None,
                    out_max_single=row['MP_OUT_MAXIMUM_S__C'] or None,
                    out_max_family=row['MP_OUT_MAXIMUM_F__C'] or None,
                    out_coin=row['MP_OUT_COINSURANCE_DEL__C'] or None,
                    rx_ded_single=row['MP_RX_DEDUCTIBLE_S__C'] or None,
                    rx_ded_family=row['MP_RX_DEDUCTIBLE_F__C'] or None,
                    rx_max_single=row['MP_RX_MAXIMUM_S__C'] or None,
                    rx_max_family=row['MP_RX_MAXIMUM_F__C'] or None,
                    rx_coin=row['MP_RX_COINSURANCE__C'] or None,
                    pcp_copay=row['MP_PCP_COPAY__C'] or None,
                    sp_copay=row['MP_SP_COPAY__C'] or None,
                    er_copay=row['MP_ER_COPAY__C'] or None,
                    uc_copay=row['MP_UC_COPAY__C'] or None,
                    lx_copay=row['MP_LX_COPAY__C'] or None,
                    ip_copay=row['MP_IP_COPAY__C'] or None,
                    op_copay=row['MP_OP_COPAY__C'] or None,
                    rx1_copay=row['MP_RX1_COPAY__C'] or None,
                    rx2_copay=row['MP_RX2_COPAY__C'] or None,
                    rx3_copay=row['MP_RX3_COPAY__C'] or None,
                    rx4_copay=row['MP_RX4_COPAY__C'] or None,
                    rx1_mail_copay=row['MP_RX1_MAIL_COPAY__C'] or None,
                    rx2_mail_copay=row['MP_RX2_MAIL_COPAY__C'] or None,
                    rx3_mail_copay=row['MP_RX3_MAIL_COPAY__C'] or None,
                    rx4_mail_copay=row['MP_RX4_MAIL_COPAY__C'] or None,
                    pcp_ded_apply=row['MP_PCP_DEDUCTIBLE_APPLY__C'] or None,
                    sp_ded_apply=row['MP_SP_DEDUCTIBLE_APPLY__C'] or None,
                    er_ded_apply=row['MP_ER_DEDUCTIBLE_APPLY__C'] or None,
                    uc_ded_apply=row['MP_UC_DEDUCTIBLE_APPLY__C'] or None,
                    lx_ded_apply=row['MP_LX_DEDUCTIBLE_APPLY__C'] or None,
                    ip_ded_apply=row['MP_IP_DEDUCTIBLE_APPLY__C'] or None,
                    op_ded_apply=row['MP_OP_DEDUCTIBLE_APPLY__C'] or None,
                    rx1_ded_apply=row['MP_RX1_DEDUCTIBLE_APPLY__C'] or None,
                    rx2_ded_apply=row['MP_RX2_DEDUCTIBLE_APPLY__C'] or None,
                    rx3_ded_apply=row['MP_RX3_DEDUCTIBLE_APPLY__C'] or None,
                    rx4_ded_apply=row['MP_RX4_DEDUCTIBLE_APPLY__C'] or None,
                    age_rated=row['AGE_RATED__C']=='TRUE',
                    hra=row['HRA__C']=='TRUE',
                    hsa=row['HSA__C']=='TRUE',
                    ded_cross=get_3_state_boolean(row['MP_DED_CROSS_ACCUMULATE__C']),
                    max_cross=get_3_state_boolean(row['MP_MAX_CROSS_ACCUMULATE__C']),
                    t1_ee=row['MP_T1_ANNUAL_EE__C'] or None,
                    t2_ee=row['MP_T2_ANNUAL_EE__C'] or None,
                    t3_ee=row['MP_T3_ANNUAL_EE__C'] or None,
                    t4_ee=row['MP_T4_ANNUAL_EE__C'] or None,
                    t1_gross=row['MP_T1_ANNUAL_GROSS__C'] or None,
                    t2_gross=row['MP_T2_ANNUAL_GROSS__C'] or None,
                    t3_gross=row['MP_T3_ANNUAL_GROSS__C'] or None,
                    t4_gross=row['MP_T4_ANNUAL_GROSS__C'] or None,
                    t1_ercdhp=row['MP_T1_ANNUAL_ERCDHP__C'] or None,
                    t2_ercdhp=row['MP_T2_ANNUAL_ERCDHP__C'] or None,
                    t3_ercdhp=row['MP_T3_ANNUAL_ERCDHP__C'] or None,
                    t4_ercdhp=row['MP_T4_ANNUAL_ERCDHP__C'] or None)
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['EMPLOYERNAME__C'])
                # break

    return HttpResponse('Successfully imported ({})!'.format(Medical.objects.all().count()))


def import_dental(request):
    path = '/home/akimmel/work/table extracts/dental.csv'
    # path = '/root/work/Enterprise/data/dental.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                dental = Dental.objects.create(          
                    title='Option D',
                    employer_id=row['EMPLOYERNAME__C'],
                    type=row['DP_TYPE__C'] or None,
                    in_ded_single=row['DP_IN_DEDUCTIBLE_S__C'] or None,
                    in_ded_family=row['DP_IN_DEDUCTIBLE_F__C'] or None,
                    in_max=row['DP_IN_MAXIMUM_PP__C'] or None,
                    in_max_ortho=row['DP_IN_ORTHO_MAXIMUM_PP__C'] or None,
                    out_ded_single=row['DP_OUT_DEDUCTIBLE_S__C'] or None,
                    out_ded_family=row['DP_OUT_DEDUCTIBLE_F__C'] or None,
                    out_max=row['DP_OUT_MAXIMUM_PP__C'] or None,
                    out_max_ortho=row['DP_OUT_ORTHO_MAXIMUM_PP__C'] or None,
                    in_prev_coin=row['DP_IN_PREV_COINSURANCE__C'] or None,
                    out_prev_coin=row['DP_OUT_PREV_COINSURANCE__C'] or None,
                    prev_ded_apply=get_3_state_boolean(row['DP_PREV_DEDUCTIBLE_APPLY__C']),
                    in_basic_coin=row['DP_IN_BASIC_COINSURANCE__C'] or None,
                    out_basic_coin=row['DP_OUT_BASIC_COINSURANCE__C'] or None,
                    basic_ded_apply=get_3_state_boolean(row['DP_BASIC_DEDUCTIBLE_APPLY__C']),
                    in_major_coin=row['DP_IN_MAJOR_COINSURANCE__C'] or None,
                    out_major_coin=row['DP_OUT_MAJOR_COINSURANCE__C'] or None,
                    major_ded_apply=get_3_state_boolean(row['DP_MAJOR_DEDUCTIBLE_APPLY__C']),
                    in_ortho_coin=row['DP_IN_ORTHO_COINSURANCE__C'] or None,
                    out_ortho_coin=row['DP_OUT_ORTHO_COINSURANCE__C'] or None,
                    ortho_ded_apply=get_3_state_boolean(row['DP_ORTHO_DEDUCTIBLE_APPLY__C']),
                    ortho_age_limit=row['DP_ORTHO_AGE_LIMIT__C'] or None,
                    t1_ee=row['DP_T1_ANNUAL_EE__C'] or None,
                    t2_ee=row['DP_T2_ANNUAL_EE__C'] or None,
                    t3_ee=row['DP_T3_ANNUAL_EE__C'] or None,
                    t4_ee=row['DP_T4_ANNUAL_EE__C'] or None,
                    t1_gross=row['DP_T1_ANNUAL_GROSS__C'] or None,
                    t2_gross=row['DP_T2_ANNUAL_GROSS__C'] or None,
                    t3_gross=row['DP_T3_ANNUAL_GROSS__C'] or None,
                    t4_gross=row['DP_T4_ANNUAL_GROSS__C'] or None)
            except Exception as e:
                print str(e)
                print '#{}#'.format(row['EMPLOYERNAME__C'])
                # break

    return HttpResponse('Successfully imported ({})!'.format(Dental.objects.all().count()))


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

    return HttpResponse('Successfully imported ({})!'.format(Dental.objects.all().count()))


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
