from django.http import JsonResponse

from .models import *
from .aux import *


"""
Medical ( PPO, HMO, HDHP ) page
"""

medical_quintile_attrs = [
]

medical_quintile_attrs_inv = [
    'in_ded_single',
    'in_max_single',
    'out_ded_single',
    'out_max_single',
    'in_coin',
    'pcp_copay',
    'er_copay',
    'lx_copay',
    'ip_copay',
    'rx1_copay',
    'rx3_copay',
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
    'rx_coin'
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

def get_medical_plan(employers, num_companies, benefit_=None):
    medians, var_local, qs = get_medical_plan_(employers, num_companies, benefit_)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'med')

    for attr in medical_attrs_boolean:
        var_local['prcnt_'+attr] = get_percent_count(qs, attr)

    for attr in medical_attrs_boolean_5_states:
        qs1 = qs.filter(**{ '{}__in'.format(attr): ['TRUE', 'True/Coin'] })
        qs2 = qs.exclude(**{ '{}__isnull'.format(attr): True })
        var_local['prcnt_'+attr] = get_percent_count_(qs1, qs2)

        qs1 = qs.filter(**{ '{}__in'.format(attr): ['False/Coin', 'True/Coin'] })
        var_local['prcnt_coin_'+attr] = get_percent_count_(qs1, qs2)

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_medical_plan_(employers, num_companies, benefit_=None):
    qs = Medical.objects.filter(employer__in=employers, type=benefit_)
    medians, sub_qs = get_medians(qs, medical_attrs_dollar, num_companies, medical_attrs_percent, medical_attrs_int)

    var_local = {}
    for attr in medical_quintile_attrs + medical_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_medical_properties(request, plan, benefit_=None):
    attrs = [item.name 
             for item in Medical._meta.fields 
             if item.name not in ['id', 'employer', 'title', 'type']]
    context = get_init_properties(attrs, medical_quintile_attrs + medical_quintile_attrs_inv)

    for attr in medical_attrs_boolean_5_states:
        context['coin_'+attr] = 'N/A'

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, qs = get_medical_plan_(employers, num_companies, benefit_)
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
        get_quintile_properties(var_local, instance, medical_quintile_attrs, medical_quintile_attrs_inv, context)

    return JsonResponse(context, safe=False)


"""
Dental ( DPPO, DMO ) page
"""

dental_quintile_attrs = [
    'in_max',
    'out_max'
]

dental_quintile_attrs_inv = [
    'in_ded_single',
    'out_ded_single',
    'in_basic_coin',
    'in_major_coin',
    'in_ortho_coin',
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

def get_dental_plan(employers, num_companies, benefit_=None):
    medians, var_local, qs = get_dental_plan_(employers, num_companies, benefit_)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'den')

    for attr in dental_attrs_boolean:
        var_local['prcnt_'+attr] = get_percent_count(qs, attr)

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_dental_plan_(employers, num_companies, benefit_=None):
    qs = Dental.objects.filter(employer__in=employers, type=benefit_)
    medians, sub_qs = get_medians(qs, dental_attrs_dollar, num_companies, dental_attrs_percent, dental_attrs_int)

    var_local = {}
    for attr in dental_quintile_attrs + dental_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_dental_properties(request, plan, benefit_=None):
    attrs = [item.name 
             for item in Dental._meta.fields 
             if item.name not in ['id', 'employer', 'title', 'type']]
    context = get_init_properties(attrs, dental_quintile_attrs + dental_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, qs = get_dental_plan_(employers, num_companies, benefit_)
        instance = Dental.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, dental_attrs_dollar, context)
        get_percent_properties(instance, dental_attrs_percent, context)
        get_int_properties(instance, dental_attrs_int, context)
        get_boolean_properties(instance, dental_attrs_boolean, context)
        get_quintile_properties(var_local, instance, dental_quintile_attrs, dental_quintile_attrs_inv, context)

    return JsonResponse(context, safe=False)


"""
VISION page
"""

vision_quintile_attrs = [
    'frames_allowance',
    'contacts_allowance'
]

vision_quintile_attrs_inv = [
    'exam_copay',
    'lenses_copay',
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

def get_vision_plan(employers, num_companies, benefit_=None):
    medians, var_local = get_vision_plan_(employers, num_companies)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'vis')

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_vision_plan_(employers, num_companies):
    qs = Vision.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, vision_attrs_dollar, num_companies, vision_attrs_percent, vision_attrs_int)

    var_local = {}
    for attr in vision_quintile_attrs + vision_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)
    return medians, var_local

def get_vision_properties(request, plan, benefit_=None):
    attrs = [item.name for item in Vision._meta.fields if item.name not in ['id', 'employer', 'title']]
    context = get_init_properties(attrs, vision_quintile_attrs + vision_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local = get_vision_plan_(employers, num_companies)
        instance = Vision.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, vision_attrs_dollar, context)
        get_percent_properties(instance, vision_attrs_percent, context)
        get_int_properties(instance, vision_attrs_int, context)
        get_quintile_properties(var_local, instance, vision_quintile_attrs, vision_quintile_attrs_inv, context)

    return JsonResponse(context, safe=False)


"""
LIFE page
"""

life_quintile_attrs = ['multiple_max', 'flat_amount']
life_quintile_attrs_inv = []
life_attrs_dollar = ['multiple_max', 'flat_amount']
life_attrs_percent = []
life_attrs_int = ['multiple']

def get_life_plan(employers, num_companies, benefit_=None):
    medians, var_local, qs = get_life_plan_(employers, num_companies)

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

def get_life_plan_(employers, num_companies):
    qs = Life.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, life_attrs_dollar, num_companies, life_attrs_percent, life_attrs_int)

    var_local = {}
    for attr in life_quintile_attrs + life_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_life_properties(request, plan, benefit_=None):
    attrs = ['multiple_max', 'flat_amount', 'multiple', 'add_flat', 'add_multiple']
    context = get_init_properties(attrs, life_quintile_attrs + life_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_life_plan_(employers, num_companies)
        instance = Life.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, life_attrs_dollar, context)
        get_float_properties(instance, life_attrs_int, context)

        if instance.type == 'Flat Amount':
            context['add_flat'] = 'Yes' if instance.add else 'No'
            attr = 'flat_amount'
        else:
            context['add_multiple'] = 'Yes' if instance.add else 'No'
            attr = 'multiple_max'
        context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

    return JsonResponse(context, safe=False)


"""
STD page
"""

std_quintile_attrs = ['weekly_max', 'duration_weeks']
std_quintile_attrs_inv = []
std_attrs_dollar = ['weekly_max']
std_attrs_percent = ['percentage']
std_attrs_int = ['waiting_days', 'waiting_days_sick', 'duration_weeks']
std_attrs_boolean = ['salary_cont']

def get_std_plan(employers, num_companies, benefit_=None):
    medians, var_local, qs = get_std_plan_(employers, num_companies)
    var_local['prcnt_salary_cont'] = get_percent_count_(qs.filter(salary_cont=True), qs)

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'std')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_std_plan_(employers, num_companies):
    qs = STD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, std_attrs_dollar, num_companies, std_attrs_percent, std_attrs_int)

    var_local = {}
    for attr in std_quintile_attrs + std_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_std_properties(request, plan, benefit_=None):
    attrs = std_attrs_dollar + std_attrs_percent + std_attrs_int + std_attrs_boolean
    context = get_init_properties(attrs, std_quintile_attrs + std_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_std_plan_(employers, num_companies)
        instance = STD.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, std_attrs_dollar, context)
        get_percent_properties(instance, std_attrs_percent, context)
        get_int_properties(instance, std_attrs_int, context)
        get_boolean_properties(instance, std_attrs_boolean, context)
        get_quintile_properties(var_local, instance, std_quintile_attrs, std_quintile_attrs_inv, context)
        
    return JsonResponse(context, safe=False)


"""
LTD page
"""

ltd_quintile_attrs = ['monthly_max']
ltd_quintile_attrs_inv = ['waiting_weeks']
ltd_attrs_dollar = ['monthly_max']
ltd_attrs_percent = ['percentage']
ltd_attrs_int = ['waiting_weeks']

def get_ltd_plan(employers, num_companies, benefit_=None):
    medians, var_local, qs = get_ltd_plan_(employers, num_companies)
    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'ltd')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_ltd_plan_(employers, num_companies):
    qs = LTD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, ltd_attrs_dollar, num_companies, ltd_attrs_percent, ltd_attrs_int)

    var_local = {}
    for attr in ltd_quintile_attrs + ltd_quintile_attrs_inv:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_ltd_properties(request, plan, benefit_=None):
    attrs = ltd_attrs_dollar + ltd_attrs_percent + ltd_attrs_int
    context = get_init_properties(attrs, ltd_quintile_attrs + ltd_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_ltd_plan_(employers, num_companies)
        instance = LTD.objects.get(id=plan)
        context['plan_info'] = ': {}, {}'.format(instance.employer.name, instance.title)
        context['client_name'] = instance.employer.name
        context['print_plan_name'] = instance.title

        get_dollar_properties(instance, ltd_attrs_dollar, context)
        get_percent_properties(instance, ltd_attrs_percent, context)
        get_int_properties(instance, ltd_attrs_int, context)
        get_quintile_properties(var_local, instance, ltd_quintile_attrs, ltd_quintile_attrs_inv, context)

    return JsonResponse(context, safe=False)


"""
STRATEGY PAGE
"""

strategy_quintile_attrs = []
strategy_quintile_attrs_inv = ['tobacco_surcharge_amount', 'spousal_surcharge_amount']
strategy_attrs_dollar = ['spousal_surcharge_amount', 'tobacco_surcharge_amount']
strategy_attrs_boolean = ['tobacco_surcharge', 'spousal_surcharge']

def get_strategy_plan(employers, num_companies, benefit_=None):
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

def get_strategy_properties(request, plan, benefit_=None):
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
