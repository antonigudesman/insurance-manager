from django.http import JsonResponse

from .models import *
from .aux import *


"""
VISION page
"""

vision_quintile_attrs = ['exam_copay',
                        'lenses_copay',
                        'frames_allowance',
                        'contacts_allowance',
                        't1_ee',
                        't1_gross']

def get_vision_plan(employers, num_companies):
    medians, var_local = get_vision_plan_(employers, num_companies)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'vis')

    return dict(var_local.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_vision_plan_(employers, num_companies):
    attrs = [item.name for item in Vision._meta.fields if item.name not in ['id', 'employer', 'title']]
    qs = Vision.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {}
    for attr in vision_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)
    return medians, var_local

def get_vision_properties(request, plan):
    context = {}
    attrs = [item.name for item in Vision._meta.fields if item.name not in ['id', 'employer', 'title']]
    for attr in attrs:
        context[attr] = 'N/A'

    for attr in vision_quintile_attrs:
        context['rank_'+attr] = 'N/A'

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local = get_vision_plan_(employers, num_companies)
        instance = Vision.objects.get(id=plan)

        for attr in attrs:
            val = getattr(instance, attr)
            context[attr] = val if val else 'N/A'

        for attr in vision_quintile_attrs:            
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

    return JsonResponse(context, safe=False)


"""
LIFE page
"""

life_quintile_attrs = ['multiple_max', 'flat_amount']

def get_life_plan(employers, num_companies):
    medians, var_local, qs = get_life_plan_(employers, num_companies)

    var_local['prcnt_add_flat'] = get_percent_count_( qs.filter(add=True, type='Flat Amount'), qs.filter(type='Flat Amount'))
    var_local['prcnt_add_multiple'] = get_percent_count_( qs.filter(add=True, type='Multiple of Salary'), qs.filter(type='Multiple of Salary'))

    # percentages for plans and cost share
    prcnt_plan_cost_share = get_plan_cost_share(qs)
    prcnt_plan_type = get_plan_type(qs)
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'life')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_type.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_life_plan_(employers, num_companies):
    attrs = ['multiple', 'multiple_max', 'flat_amount']
    qs = Life.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {}
    for attr in life_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_life_properties(request, plan):
    context = {
        'multiple_max': 'N/A',
        'flat_amount': 'N/A',
        'multiple': 'N/A',
        'add_flat': 'N/A',
        'add_multiple': 'N/A',
        'rank_flat_amount': 'N/A',
        'rank_multiple_max': 'N/A'    
    }

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local, _ = get_life_plan_(employers, num_companies)
        instance = Life.objects.get(id=plan)

        context['multiple_max'] = '${:,.0f}'.format(instance.multiple_max) if instance.multiple_max else 'N/A'
        context['flat_amount'] = '${:,.0f}'.format(instance.flat_amount) if instance.flat_amount else 'N/A'
        context['multiple'] = '{:03.1f}'.format(instance.multiple) if instance.multiple else 'N/A'

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

def get_std_plan(employers, num_companies):
    medians, var_local, qs = get_std_plan_(employers, num_companies)
    var_local['prcnt_salary_cont'] = qs.filter(salary_cont=True).count() * 100 / qs.count()

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'std')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_std_plan_(employers, num_companies):
    attrs = ['waiting_days', 'waiting_days_sick', 'weekly_max', 'percentage', 'duration_weeks']
    qs = STD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {}
    for attr in std_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_std_properties(request, plan):
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

def get_ltd_plan(employers, num_companies):
    medians, var_local, qs = get_ltd_plan_(employers, num_companies)
    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'ltd')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())

def get_ltd_plan_(employers, num_companies):
    attrs = ['waiting_weeks', 'monthly_max', 'percentage']
    qs = LTD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {}
    for attr in ltd_quintile_attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    return medians, var_local, qs

def get_ltd_properties(request, plan):
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

        for attr in ltd_quintile_attrs:            
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

        context['monthly_max'] = '${:,.0f}'.format(instance.monthly_max) if instance.monthly_max else 'N/A'
        context['percentage'] = '{:,.0f}%'.format(instance.percentage) if instance.percentage else 'N/A'
        context['waiting_weeks'] = '{:,.0f}'.format(instance.waiting_weeks) if instance.waiting_weeks else 'N/A'
        
    return JsonResponse(context, safe=False)


"""
STRATEGY PAGE
"""

strategy_quintile_attrs = ['tobacco_surcharge_amount', 'spousal_surcharge_amount']

def get_strategy_plan(employers, num_companies):
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

def get_strategy_properties(request, plan):
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
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

        context['spousal_surcharge_amount'] = '${:,.0f}'.format(instance.spousal_surcharge_amount) if instance.spousal_surcharge_amount else 'N/A'
        context['tobacco_surcharge_amount'] = '${:,.0f}'.format(instance.tobacco_surcharge_amount) if instance.tobacco_surcharge_amount else 'N/A'
        context['tobacco_surcharge'] = 'Yes' if instance.tobacco_surcharge else 'No'
        context['spousal_surcharge'] = 'Yes' if instance.spousal_surcharge else 'No'
        
    return JsonResponse(context, safe=False)