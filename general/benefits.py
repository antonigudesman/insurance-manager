from django.http import JsonResponse
from django.utils.safestring import SafeString

import HTMLParser

from .models import *
from .aux import *
import json
import pdb
import logging
log = logging.getLogger(__name__)

"""
Medical ( PPO, HMO, HDHP ) page
"""

medical_quintile_attrs = [
]

medical_quintile_attrs_inv = [
    'in_ded_single',
    'out_ded_single',
    't1_ee',
    't1_gross'
]

medical_attrs_dollar = [
    'in_ded_single',
    'in_ded_family',
    'in_max_single',
    'in_max_family',
    'out_ded_single',
    'out_ded_family',
    'out_max_single',
    'out_max_family',
    'rx_ded_single',
    'rx_ded_family',
    'rx_max_single',
    'rx_max_family',
    'pcp_copay',
    'sp_copay',
    'er_copay',
    'uc_copay',
    'lx_copay',
    'op_copay',
    'ip_copay',
    'rx1_copay',
    'rx1_mail_copay',
    'rx2_copay',
    'rx2_mail_copay',
    'rx3_copay',
    'rx3_mail_copay',
    'rx4_copay',
    'rx4_mail_copay',
    't1_ee',
    't2_ee',
    't3_ee',
    't4_ee',
    't1_gross',
    't2_gross',
    't3_gross',
    't4_gross',
    't1_ercdhp',
    't2_ercdhp',
    't3_ercdhp',
    't4_ercdhp'
]

medical_attrs_percent = [
    'in_coin',
    'out_coin',
    'rx_coin',
]

medical_attrs_int = []

medical_attrs_boolean = [
    'ded_cross',
    'max_cross',
    'hra',
    'hsa',
    'age_rated'
]

medical_attrs_boolean_5_states = [
    'pcp_ded_apply',
    'sp_ded_apply',
    'er_ded_apply',
    'uc_ded_apply',
    'lx_ded_apply',
    'op_ded_apply',
    'ip_ded_apply',
    'rx1_ded_apply',
    'rx2_ded_apply',
    'rx3_ded_apply',
    'rx4_ded_apply',
]

medical_services = [
    'PCP',
    'IP',
    'Rx1'
]

def get_medicalrx_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('MEDICALRX_quintile_properties') or medical_quintile_attrs
    quintile_properties_inv = request.session.get('MEDICALRX_quintile_properties_inv') or medical_quintile_attrs_inv
    services = request.session.get('MEDICALRX_services') or medical_services
    
    medians, var_local, qs = get_medical_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'med')

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)
    var_local['services'] = json.dumps(services)

    log.debug(quintile_properties_inv)

    num_t = Medical.objects.filter(employer__in=employers, type__in=['PPO', 'POS']).values('employer_id').distinct()
    var_local['prcnt_ppo'] = '{:,.0f}%'.format(len(num_t) * 100 / num_companies)
    num_t = Medical.objects.filter(employer__in=employers, type__in=['HMO', 'EPO']).values('employer_id').distinct()
    var_local['prcnt_hmo'] = '{:,.0f}%'.format(len(num_t) * 100 / num_companies)
    num_t = Medical.objects.filter(employer__in=employers, type__in=['HDHP']).values('employer_id').distinct()
    var_local['prcnt_hdhp'] = '{:,.0f}%'.format(len(num_t) * 100 / num_companies)

    plan_types = get_real_medical_type(plan_type)
    num_tt = Medical.objects.filter(employer__in=employers, type__in=plan_types).count() or 1
    num_t = Medical.objects.filter(employer__in=employers, type__in=plan_types, rx_ded_single__isnull=False,rx_ded_single__gt=0).count()
    var_local['prcnt_rx_ded_single'] = '{:,.0f}%'.format(num_t * 100 / num_tt)
    num_t = Medical.objects.filter(employer__in=employers, type__in=plan_types, rx_max_single__isnull=False, rx_max_single__gt=0).count()
    var_local['prcnt_rx_max_single'] = '{:,.0f}%'.format(num_t * 100 / num_tt)

    for attr in medical_attrs_boolean:
        var_local['prcnt_'+attr] = get_percent_count(qs, attr)

    for attr in medical_attrs_boolean_5_states:
        qs1 = qs.filter(**{ '{}__in'.format(attr): ['TRUE', 'True/Coin'] })
        qs2 = qs.exclude(**{ '{}__isnull'.format(attr): True })
        var_local['prcnt_'+attr] = get_percent_count_(qs1, qs2)

        qs1 = qs.filter(**{ '{}__in'.format(attr): ['False/Coin', 'True/Coin'] })
        var_local['prcnt_coin_'+attr] = get_percent_count_(qs1, qs2)

    # calculate employee costs
    for service in settings.CPT_COST.keys():
        e_costs, e_stacks = employee_pricing_medical(qs, service)
        val, idx = get_median_list(e_costs)
        var_local[service+'_attr'] = e_stacks[idx]

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_medical_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):    
    plan_type = get_real_medical_type(plan_type)
    qs = Medical.objects.filter(employer__in=employers, type__in=plan_type) 
    medians, sub_qs = get_medians(qs, medical_attrs_dollar, num_companies, medical_attrs_percent, medical_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr, 'medicalrx')
        idx += 1

    return medians, var_local, qs

def get_medical_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    quintile_properties = quintile_properties or medical_quintile_attrs
    quintile_properties_inv = quintile_properties_inv or medical_quintile_attrs_inv
    services = services or medical_services
    attrs = [item.name 
             for item in Medical._meta.fields 
             if item.name not in ['id', 'employer', 'title', 'type']]
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)

    for attr in medical_attrs_boolean_5_states:
        context['coin_'+attr] = ''

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, qs = get_medical_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
        instance = Medical.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, medical_attrs_dollar, context)
        get_percent_properties(instance, medical_attrs_percent, context)
        get_int_properties(instance, medical_attrs_int, context)
        get_boolean_properties(instance, medical_attrs_boolean, context)
        get_boolean_properties_5_states(instance, medical_attrs_boolean_5_states, context)
        get_boolean_properties_5_states_coin(instance, medical_attrs_boolean_5_states, context)
        print var_local, '@@@@@@@@@@@@'
        get_quintile_properties_idx(var_local, instance, quintile_properties, quintile_properties_inv, context)

        # calculate employee costs
        for service in settings.CPT_COST.keys():
            val, e_stacks = employee_pricing_medical([instance], service)
            context['service_'+service] = e_stacks[0] if e_stacks else None

        for service in services:
            val, e_stacks = employee_pricing_medical([instance], service)            
            e_costs, e_stacks = employee_pricing_medical(qs, service)
            percentile_array = get_incremental_array_(len(e_costs), sorted(e_costs))

            val = val[0] if val else None
            rank = get_rank(percentile_array, val)
            if rank != '-':
                rank = 100 - rank
            context['rank_'+service] = rank


    return JsonResponse(context, safe=False)


def get_real_medical_type(plan_type):
    if plan_type == 'PPO':
        plan_type = ['PPO', 'POS']
    elif plan_type == 'HMO':
        plan_type = ['HMO', 'EPO']
    else:
        plan_type = ['HDHP']

    return plan_type


def get_attr_quintile(benefit, employers, num_companies, plan_type, attr, MODEL_MAP, plan, inverse):
    if benefit == 'MEDICALRX':
        plan_type = get_real_medical_type(plan_type)
        model = MODEL_MAP['MEDICAL']
    else:
        plan_type = [plan_type]
        model = MODEL_MAP[benefit]

    qs = model.objects.filter(employer__in=employers)
    # pdb.set_trace()
    if plan_type and not 'All' in plan_type:
        qs = qs.filter(type__in=plan_type) 

    kwargs = { '{0}__isnull'.format(attr): True }
    sub_qs = qs.exclude(**kwargs)
    quintile = get_incremental_array(sub_qs, attr, benefit.lower())

    val = 0
    qscore = 'N/A'    
    if plan > 0:
        instance = model.objects.get(id=plan)
        val = getattr(instance, attr)
        qscore = get_rank(quintile, getattr(instance, attr))
        print qscore, inverse, '@@@@@@@@'
        if qscore != '-':
            qscore = qscore if not inverse else 100 - qscore

    return quintile, qscore, val

"""
Dental ( DPPO, DMO ) page
"""

dental_quintile_attrs = [
    'in_max',
]

dental_quintile_attrs_inv = [
    'in_ded_single',
    't1_ee',
    't1_gross'
]

dental_attrs_dollar = [
    'in_ded_single',
    'in_ded_family',
    'in_max',
    'in_max_ortho',
    'out_ded_single',
    'out_ded_family',
    'out_max',
    'out_max_ortho',
    't1_ee',
    't2_ee',
    't3_ee',
    't4_ee',
    't1_gross',
    't2_gross',
    't3_gross',
    't4_gross'
]

dental_attrs_percent = [
    'in_prev_coin',
    'out_prev_coin',
    'in_basic_coin',
    'out_basic_coin',
    'in_major_coin',
    'out_major_coin',
    'in_ortho_coin',
    'out_ortho_coin',
]

dental_attrs_int = ['ortho_age_limit']

dental_attrs_boolean = [
    'prev_ded_apply',
    'basic_ded_apply',
    'major_ded_apply',
    'ortho_ded_apply'
]

def get_dental_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('DENTAL_quintile_properties') or dental_quintile_attrs
    quintile_properties_inv = request.session.get('DENTAL_quintile_properties_inv') or dental_quintile_attrs_inv
    # services = request.session.get('DENTAL_services') or dental_services
    
    medians, var_local, qs = get_dental_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'den')

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)
    # var_local['services'] = json.dumps(services)

    num_t = Dental.objects.filter(employer__in=employers, type__in=['DPPO']).values('employer_id').distinct()
    var_local['prcnt_dppo'] = '{:,.0f}%'.format(len(num_t) * 100 / num_companies)
    num_t = Dental.objects.filter(employer__in=employers, type__in=['DMO']).values('employer_id').distinct()
    var_local['prcnt_dmo'] = '{:,.0f}%'.format(len(num_t) * 100 / num_companies)

    num_tt = Dental.objects.filter(employer__in=employers, type=plan_type).count() or 1
    num_t = Dental.objects.filter(employer__in=employers, type=plan_type, ortho_ded_apply__isnull=False, ortho_ded_apply__gt=0).count()
    var_local['pprcnt_ortho_ded_apply'] = '{:,.0f}%'.format(num_t * 100 / num_tt)
    num_t = Dental.objects.filter(employer__in=employers, type=plan_type, ortho_age_limit__isnull=False, ortho_age_limit__gt=0).count()
    var_local['pprcnt_ortho_age_limit'] = '{:,.0f}%'.format(num_t * 100 / num_tt)

    for attr in dental_attrs_boolean:
        var_local['prcnt_'+attr] = get_percent_count(qs, attr)

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_dental_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):
    qs = Dental.objects.filter(employer__in=employers, type=plan_type)
    medians, sub_qs = get_medians(qs, dental_attrs_dollar, num_companies, dental_attrs_percent, dental_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr)
        idx += 1

    return medians, var_local, qs

def get_dental_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = [item.name 
             for item in Dental._meta.fields 
             if item.name not in ['id', 'employer', 'title', 'type']]
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)
    # pdb.set_trace()
    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        instance = Dental.objects.get(id=plan)
        medians, var_local, qs = get_dental_plan_(employers, num_companies, instance.type, quintile_properties, quintile_properties_inv)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, dental_attrs_dollar, context)
        get_percent_properties(instance, dental_attrs_percent, context)
        get_int_properties(instance, dental_attrs_int, context)
        get_boolean_properties(instance, dental_attrs_boolean, context)
        get_quintile_properties_idx(var_local, instance, quintile_properties, quintile_properties_inv, context)

    return JsonResponse(context, safe=False)


"""
VISION page
"""

vision_quintile_attrs = [
]

vision_quintile_attrs_inv = [
    'exam_copay',
    't1_ee',
    't1_gross'
]

vision_attrs_dollar = [
    'exam_copay',
    'exam_out_allowance',
    'lenses_copay',
    'lenses_out_allowance',
    'frames_copay',
    'frames_allowance',
    'frames_out_allowance',
    'contacts_copay',
    'contacts_allowance',
    'contacts_out_allowance',
    't1_ee',
    't2_ee',
    't3_ee',
    't4_ee',
    't1_gross',
    't2_gross',
    't3_gross',
    't4_gross'
]

vision_attrs_percent = [
    'frames_coinsurance',
    'contacts_coinsurance'
]

vision_attrs_int = [
    'exam_frequency',
    'lenses_frequency',
    'frames_frequency',
    'contacts_frequency'
]

def get_vision_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('VISION_quintile_properties') or vision_quintile_attrs
    quintile_properties_inv = request.session.get('VISION_quintile_properties_inv') or vision_quintile_attrs_inv
    # services = request.session.get('DENTAL_services') or dental_services
    
    medians, var_local = get_vision_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'vis')

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_vision_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):
    qs = Vision.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, vision_attrs_dollar, num_companies, vision_attrs_percent, vision_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr)
        idx += 1
    return medians, var_local

def get_vision_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = [item.name for item in Vision._meta.fields if item.name not in ['id', 'employer', 'title']]
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local = get_vision_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
        instance = Vision.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, vision_attrs_dollar, context)
        get_percent_properties(instance, vision_attrs_percent, context)
        get_int_properties(instance, vision_attrs_int, context)
        get_quintile_properties_idx(var_local, instance, quintile_properties, quintile_properties_inv, context)

    return JsonResponse(context, safe=False)


"""
LIFE page
"""

life_quintile_attrs = ['multiple_max', 'flat_amount']
life_quintile_attrs_inv = []
life_attrs_dollar = ['multiple_max', 'flat_amount']
life_attrs_percent = []
life_attrs_int = ['multiple']

def get_life_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('LIFE_quintile_properties') or life_quintile_attrs
    quintile_properties_inv = request.session.get('LIFE_quintile_properties_inv') or life_quintile_attrs_inv
    # services = request.session.get('DENTAL_services') or dental_services
    
    medians, var_local, qs = get_life_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)
    

    var_local['prcnt_add_flat'] = get_percent_count_( qs.filter(add=True, type='Flat Amount'), qs.filter(type='Flat Amount'))
    var_local['prcnt_add_multiple'] = get_percent_count_( qs.filter(add=True, type='Multiple of Salary'), qs.filter(type='Multiple of Salary'))

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'life')
    prcnt_plan_type = get_plan_type(qs)
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_type.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_life_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):
    qs = Life.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, life_attrs_dollar, num_companies, life_attrs_percent, life_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr)
        idx += 1

    return medians, var_local, qs

def get_life_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = ['multiple_max', 'flat_amount', 'multiple', 'add_flat', 'add_multiple']
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_life_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
        instance = Life.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, life_attrs_dollar, context)
        get_float_properties(instance, life_attrs_int, context)

        if instance.type == 'Flat Amount':
            context['add_flat'] = 'Yes' if instance.add else 'No'
            attr = 'flat_amount'
            idx = 1
        else:
            context['add_multiple'] = 'Yes' if instance.add else 'No'
            attr = 'multiple_max'
            idx = 0
        context['rank_'+attr] = get_rank(var_local['quintile_'+str(idx)], getattr(instance, attr))

    return JsonResponse(context, safe=False)


"""
STD page
"""

std_quintile_attrs = ['weekly_max']
std_quintile_attrs_inv = []
std_attrs_dollar = ['weekly_max']
std_attrs_percent = ['percentage']
std_attrs_int = ['waiting_days', 'waiting_days_sick', 'duration_weeks']
std_attrs_boolean = ['salary_cont']

def get_std_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('STD_quintile_properties') or std_quintile_attrs
    quintile_properties_inv = request.session.get('STD_quintile_properties_inv') or std_quintile_attrs_inv
    # services = request.session.get('DENTAL_services') or dental_services
    
    medians, var_local, qs = get_std_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)

    var_local['prcnt_salary_cont'] = get_percent_count_(qs.filter(salary_cont=True), qs)

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'std')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_std_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):
    qs = STD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, std_attrs_dollar, num_companies, std_attrs_percent, std_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr)
        idx += 1

    return medians, var_local, qs

def get_std_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = std_attrs_dollar + std_attrs_percent + std_attrs_int + std_attrs_boolean
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_std_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
        instance = STD.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, std_attrs_dollar, context)
        get_percent_properties(instance, std_attrs_percent, context)
        get_int_properties(instance, std_attrs_int, context)
        get_boolean_properties(instance, std_attrs_boolean, context)
        get_quintile_properties_idx(var_local, instance, quintile_properties, quintile_properties_inv, context)
        
    return JsonResponse(context, safe=False)


"""
LTD page
"""

ltd_quintile_attrs = ['monthly_max']
ltd_quintile_attrs_inv = []
ltd_attrs_dollar = ['monthly_max']
ltd_attrs_percent = ['percentage']
ltd_attrs_int = ['waiting_weeks']

def get_ltd_plan(request, employers, num_companies, plan_type=None):
    quintile_properties = request.session.get('LTD_quintile_properties') or ltd_quintile_attrs
    quintile_properties_inv = request.session.get('LTD_quintile_properties_inv') or ltd_quintile_attrs_inv
    # services = request.session.get('DENTAL_services') or dental_services
    
    medians, var_local, qs = get_ltd_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)

    h = HTMLParser.HTMLParser()
    var_local['quintile_properties'] = json.dumps(quintile_properties)
    var_local['quintile_properties_inv'] = json.dumps(quintile_properties_inv)

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'ltd')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_ltd_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv):
    qs = LTD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, ltd_attrs_dollar, num_companies, ltd_attrs_percent, ltd_attrs_int)

    var_local = {}
    idx = 0
    for attr in quintile_properties + quintile_properties_inv:
        var_local['quintile_'+str(idx)] = get_incremental_array(sub_qs['qs_'+attr], attr)
        print var_local['quintile_'+str(idx)], '##############'
        idx += 1

    return medians, var_local, qs

def get_ltd_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = ltd_attrs_dollar + ltd_attrs_percent + ltd_attrs_int
    context = get_init_properties(attrs, quintile_properties + quintile_properties_inv)
    
    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_ltd_plan_(employers, num_companies, plan_type, quintile_properties, quintile_properties_inv)
        instance = LTD.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, ltd_attrs_dollar, context)
        get_percent_properties(instance, ltd_attrs_percent, context)
        get_int_properties(instance, ltd_attrs_int, context)
        get_quintile_properties_idx(var_local, instance, quintile_properties, quintile_properties_inv, context)

    return JsonResponse(context, safe=False)


"""
STRATEGY PAGE
"""

strategy_quintile_attrs = []
strategy_quintile_attrs_inv = []
strategy_attrs_dollar = ['spousal_surcharge_amount', 'tobacco_surcharge_amount']
strategy_attrs_boolean = ['tobacco_surcharge', 'spousal_surcharge']

def get_strategy_plan(request, employers, num_companies, plan_type=None):
    medians, var_local, qs = get_strategy_plan_(employers, num_companies)

    attrs = ['spousal_surcharge',
             'tobacco_surcharge',
             'offer_vol_life',
             'offer_vol_std',
             'offer_vol_ltd',
             'pt_medical',
             'pt_dental',
             'pt_vision',
             'pt_life',
             'pt_std',
             'pt_ltd',
             'defined_contribution',
             'salary_banding',
             'wellness_banding',
             'offer_fsa',
             'narrow_network',
             'mvp',
             'mec']

    for attr in attrs:
        var_local['prcnt_'+attr] = get_percent_count(qs, attr)

    return dict(var_local.items() 
              + medians.items())

def get_strategy_plan_(employers, num_companies):
    qs = Strategy.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, strategy_attrs_dollar, num_companies)
    
    var_local = {}
    for attr in strategy_quintile_attrs + strategy_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)
    return medians, var_local, qs

def get_strategy_properties(request, plan, plan_type, quintile_properties, quintile_properties_inv, services=[]):
    attrs = strategy_attrs_dollar + strategy_attrs_boolean
    context = get_init_properties(attrs, strategy_quintile_attrs + strategy_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, qs = get_strategy_plan_(employers, num_companies)
        instance = Strategy.objects.get(id=plan)
        context['plan_info'] = ': {}'.format(instance.employer.name)
        context['client_name'] = instance.employer.name

        get_dollar_properties(instance, strategy_attrs_dollar, context)
        get_boolean_properties(instance, strategy_attrs_boolean, context)
        get_quintile_properties(var_local, instance, strategy_quintile_attrs, strategy_quintile_attrs_inv, context)
        
    return JsonResponse(context, safe=False)


ATTRIBUTE_MAP = {
    'MEDICAL': [
        {
            'attrs': ['in_ded_single', 'in_ded_family', 'in_max_single', 'in_max_family', 'in_coin', 'rx_coin'],             
            'class': 'property_inv'
        },
        {
            'attrs': ['out_ded_single', 'out_ded_family', 'out_max_single', 'out_max_family', 'out_coin'],
            'class': 'property_inv'
        },
        {
            'attrs': ['t1_ee', 't2_ee', 't3_ee', 't4_ee'],
            'class': 'property_inv'
        },
        {
            'attrs': ['t1_gross', 't2_gross', 't3_gross', 't4_gross'],
            'class': 'property_inv'
        },
        {
            'attrs': ['PCP', 'SP', 'LX'],
            'class': 'service'
        },
        {
            'attrs': ['IP', 'OP', 'ER', 'UC'],
            'class': 'service'
        },
        {
            'attrs': ['Rx1', 'Rx2', 'Rx3', 'Rx4'],
            'class': 'service'
        }],
    'DENTAL': [
        {
            'attrs': ['in_ded_single', 'in_ded_family', 'out_ded_single', 'out_ded_family'],
            'class': 'property_inv'
        },
        {
            'attrs': ['in_max', 'in_max_ortho', 'out_max', 'out_max_ortho'],
            'class': 'property'
        },
        {
            'attrs': ['t1_ee', 't2_ee', 't3_ee', 't4_ee'],
            'class': 'property_inv'
        },
        {
            'attrs': ['t1_gross', 't2_gross', 't3_gross', 't4_gross'],
            'class': 'property_inv'
        }],
    'VISION': [
        {
            'attrs': ['exam_copay', 'lenses_copay', 'contacts_copay', 'frames_copay', 'frames_allowance', 'contacts_allowance'],
            'class': 'property_inv'
        },
        {
            'attrs': ['t1_ee', 't2_ee', 't3_ee', 't4_ee'],
            'class': 'property_inv'
        },
        {
            'attrs': ['t1_gross', 't2_gross', 't3_gross', 't4_gross'],
            'class': 'property_inv'
        }],
    'STD': [
        {
            'attrs': ['weekly_max', 'percentage'],
            'class': 'property'
        }],
    'LTD': [
        {
            'attrs': ['monthly_max', 'percentage'],
            'class': 'property'
        }],
    'LIFE': [
        {
            'attrs': ['multiple_max'],
            'class': 'property'
        },
        {
            'attrs': ['flat_amount'],
            'class': 'property'
        }],
    'STRATEGY': []
}
