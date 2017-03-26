from django.http import JsonResponse

from .models import *
from .aux import *


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
    'in_prev_coin',
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
    for attr in life_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_life_properties(request, plan, benefit_=None):
    attrs = ['multiple_max', 'flat_amount', 'multiple', 'add_flat', 'add_multiple']
    context = get_init_properties(attrs, life_quintile_attrs + life_quintile_attrs_inv)

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_life_plan_(employers, num_companies)
        instance = Life.objects.get(id=plan)

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
    attrs = ['weekly_max']
    attrs_percent = ['percentage']
    attrs_int = ['waiting_days', 'waiting_days_sick', 'duration_weeks']

    qs = STD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies, attrs_percent, attrs_int)

    var_local = {}
    for attr in std_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_std_properties(request, plan, benefit_=None):
    context = {
        'weekly_max': 'N/A',
        'percentage': 'N/A',
        'salary_cont': 'N/A',
        'duration_weeks': 'N/A',
        'waiting_injury': 'N/A',
        'waiting_illness': 'N/A',
        'rank_weekly_max': 'N/A',
        'rank_duration_weeks': 'N/A'
    }

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_std_plan_(employers, num_companies)
        instance = STD.objects.get(id=plan)

        for attr in std_quintile_attrs:            
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

        context['weekly_max'] = '${:,.0f}'.format(instance.weekly_max) if instance.weekly_max else 'N/A'
        context['percentage'] = '{:,.0f}%'.format(instance.percentage) if instance.percentage else 'N/A'
        context['duration_weeks'] = '{:,.0f}'.format(instance.duration_weeks) if instance.duration_weeks else 'N/A'
        context['waiting_injury'] = '{:,.0f}'.format(instance.waiting_days) if instance.waiting_days else 'N/A'
        context['waiting_illness'] = '{:,.0f}'.format(instance.waiting_days_sick) if instance.waiting_days_sick else 'N/A'
        context['salary_cont'] = 'Yes' if instance.salary_cont else 'No'
        
    return JsonResponse(context, safe=False)


"""
LTD page
"""

ltd_quintile_attrs = ['waiting_weeks', 'monthly_max']

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
    attrs = ['monthly_max']
    attrs_percent = ['percentage']
    attrs_int = ['waiting_weeks']

    qs = LTD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies, attrs_percent, attrs_int)

    var_local = {}
    for attr in ltd_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_ltd_properties(request, plan, benefit_=None):
    context = {
        'monthly_max': 'N/A',
        'percentage': 'N/A',
        'waiting_weeks': 'N/A',
        'rank_monthly_max': 'N/A',
        'rank_waiting_weeks': 'N/A'
    }

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_ltd_plan_(employers, num_companies)
        instance = LTD.objects.get(id=plan)

        for attr in ['monthly_max']:            
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

        for attr in ['waiting_weeks']:         
            rank = get_rank(var_local['quintile_'+attr], getattr(instance, attr))
            context['rank_'+attr] = rank if rank == 'N/A' else 6 - rank

        context['monthly_max'] = '${:,.0f}'.format(instance.monthly_max) if instance.monthly_max else 'N/A'
        context['percentage'] = '{:,.0f}%'.format(instance.percentage) if instance.percentage else 'N/A'
        context['waiting_weeks'] = '{:,.0f}'.format(instance.waiting_weeks) if instance.waiting_weeks else 'N/A'
        
    return JsonResponse(context, safe=False)


"""
STRATEGY PAGE
"""

strategy_quintile_attrs = ['tobacco_surcharge_amount', 'spousal_surcharge_amount']

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
    medians, sub_qs = get_medians(qs, strategy_quintile_attrs, num_companies)
    
    var_local = {}
    for attr in strategy_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)
    return medians, var_local, qs

def get_strategy_properties(request, plan, benefit_=None):
    context = {
        'tobacco_surcharge_amount': 'N/A',
        'tobacco_surcharge': 'N/A',
        'spousal_surcharge_amount': 'N/A',
        'spousal_surcharge': 'N/A',
        'rank_spousal_surcharge_amount': 'N/A',
        'rank_tobacco_surcharge_amount': 'N/A'    
    }

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, qs = get_strategy_plan_(employers, num_companies)
        instance = Strategy.objects.get(id=plan)

        for attr in strategy_quintile_attrs:       
            rank = get_rank(var_local['quintile_'+attr], getattr(instance, attr))
            context['rank_'+attr] = rank if rank == 'N/A' else 6 - rank

        context['spousal_surcharge_amount'] = '${:,.0f}'.format(instance.spousal_surcharge_amount) if instance.spousal_surcharge_amount else 'N/A'
        context['tobacco_surcharge_amount'] = '${:,.0f}'.format(instance.tobacco_surcharge_amount) if instance.tobacco_surcharge_amount else 'N/A'
        context['tobacco_surcharge'] = 'Yes' if instance.tobacco_surcharge else 'No'
        context['spousal_surcharge'] = 'Yes' if instance.spousal_surcharge else 'No'
        
    return JsonResponse(context, safe=False)
