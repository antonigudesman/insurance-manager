import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.db.models import Q, Avg, StdDev
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import *


HEAD_COUNT = {
    'Up to 250': [0, 249],
    '250 to 499': [250, 499],
    '500 to 999': [500, 999],
    '1,000 to 4,999': [1000, 4999],
    '5,000 and Up': [5000, 2000000],
}

MODEL_MAP = {
    'LIFE': Life,
    'STD': STD,
    'LTD': LTD,
    'STRATEGY': Strategy, 
    'VISION': Vision
}

PLAN_ALLOWED_BENEFITS = ['LIFE', 'STD', 'LTD', 'STRATEGY', 'VISION']

def get_filtered_employers(ft_industries, ft_head_counts, ft_other, ft_regions, lstart=0, lend=0, group='bnchmrk'):
    # filter with factors from UI (industry, head-count, other)
    q = Q()
    if not '*' in ft_industries:
        q = Q(industry1__in=ft_industries) | Q(industry2__in=ft_industries) | Q(industry3__in=ft_industries)

    for item in ft_other:
        if item != '*':
            q &= Q(**{item: True})

    q_region = Q()
    if not '*' in ft_regions:
        for item in ft_regions:
            q_region |= Q(**{item: True})

    q &= q_region
    q_ = Q(size=0)
    for ft_head_count in ft_head_counts:
        ft_vals = ft_head_count.split('-')        
        q_ |= Q(size__gte=int(ft_vals[0])) & Q(size__lte=int(ft_vals[1]))


    if group == "bnchmrk":
        employers_ = Employer.objects.filter(q & q_).order_by('name')
    else:
        select = {'new_name':
            'CASE WHEN broker=\'Core\' THEN name WHEN broker=\'{}\' THEN name ELSE \'De-identified Employer\' END'.format(group)}
        employers_ = Employer.objects.filter(q & q_).extra(select=select).order_by('new_name')
        
    employers = employers_
    if lend:
        employers = employers_[lstart:lend]

    num_companies = Employer.objects.filter(q & q_).count()    
    # filter with number of companies
    if num_companies < settings.EMPLOYER_THRESHOLD:
        employers = []
        # num_companies = 0

    return employers, num_companies


@csrf_exempt
@login_required(login_url='/admin/login')
def enterprise(request):
    """
    GET: render general enterprise page
    POST: for enterprise bootgrid table
    """
    if request.method == 'POST':
        form_param = json.loads(request.body or "{}")
        limit = int(form_param.get('rowCount'))
        page = int(form_param.get('current'))
        ft_industries = form_param.get('industry_') or ['*']
        ft_head_counts = form_param.get('head_counts') or ['0-2000000']
        ft_other = form_param.get('others')
        ft_regions = form_param.get('regions')

        lstart = (page - 1) * limit
        lend = lstart + limit

        group = request.user.groups.first().name

        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other, 
                                                          ft_regions, 
                                                          lstart, 
                                                          lend,
                                                          group)

        # convert head-count into groups
        employers_ = []
        for item in employers:
            item_ = model_to_dict(item)

            if group != 'bnchmrk':
                item_['name'] = item.new_name

            item__ = []
            if item.nonprofit:
                item__.append('Non-Profit')
            if item.govt_contractor:
                item__.append("Gov't Contractor")
            item_['other'] = '@'.join(item__)

            item__ = []
            if item.industry1:
                item__.append(item.industry1)
            if item.industry2:
                item__.append(item.industry2)
            if item.industry3:
                item__.append(item.industry3)
            item_['industry'] = '@'.join(item__)

            item__ = []
            if item.new_england:
                item__.append('New England')
            if item.mid_atlantic:
                item__.append('Tri-State Area')
            if item.south_atlantic:
                item__.append('South Atlantic')
            if item.south_cental:
                item__.append('South Central')
            if item.east_central:
                item__.append('East North Central')
            if item.west_central:
                item__.append('West North Central')
            if item.mountain:
                item__.append('Mountian')
            if item.pacific:
                item__.append('Pacific')
            item_['region'] = '@'.join(item__)

            for key, val in HEAD_COUNT.items():
                if item.size in range(val[0], val[1]):
                    item_['size'] = key
                    break
            employers_.append(item_)

        if num_companies < settings.EMPLOYER_THRESHOLD:
            num_companies = 0

        return JsonResponse({
            "current": page,
            "rowCount": limit,
            "rows": employers_,
            "total": num_companies
            }, safe=False)
    else:
        # get valid distinct industries 
        industries1 = Employer.objects.order_by('industry1').values_list('industry1').distinct()
        industries1 = [item[0] for item in industries1 if item[0]]
        industries2 = Employer.objects.order_by('industry2').values_list('industry2').distinct()
        industries2 = [item[0] for item in industries2 if item[0]]
        industries3 = Employer.objects.order_by('industry3').values_list('industry3').distinct()
        industries3 = [item[0] for item in industries3 if item[0]]
        industries = set(industries1 + industries2 + industries3)

        request.session['benefit'] = request.session.get('benefit', 'HOME')

        return render(request, 'enterprise.html', {
                'industries': sorted(industries),
                'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE
            })
        

@csrf_exempt
def ajax_enterprise(request):
    """
    get body of page
    supposed to be called for only real template not print
    """
    form_param = request.POST
    ft_industries = form_param.getlist('industry[]', ['*'])
    ft_head_counts = form_param.getlist('head_counts[]') or ['0-2000000']
    ft_other = form_param.getlist('others[]')
    ft_regions = form_param.getlist('regions[]')

    ft_industries_label = form_param.getlist('industry_label[]')
    ft_head_counts_label = form_param.getlist('head_counts_label[]')
    ft_other_label = form_param.getlist('others_label[]')
    ft_regions_label = form_param.getlist('regions_label[]')

    benefit = form_param.get('benefit')

    # store for print
    request.session['benefit'] = benefit
    request.session['ft_industries'] = ft_industries
    request.session['ft_head_counts'] = ft_head_counts
    request.session['ft_other'] = ft_other
    request.session['ft_regions'] = ft_regions

    request.session['ft_industries_label'] = ft_industries_label
    request.session['ft_head_counts_label'] = ft_head_counts_label
    request.session['ft_other_label'] = ft_other_label
    request.session['ft_regions_label'] = ft_regions_label

    today = datetime.strftime(datetime.now(), '%B %d, %Y')

    if benefit == 'HOME':
        full_name = '{} {}'.format(request.user.first_name, request.user.last_name)
        return render(request, 'benefit/home.html', locals())
    elif benefit in ['LIFE', 'STD', 'LTD', 'STRATEGY', 'VISION']:
        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)

        if num_companies < settings.EMPLOYER_THRESHOLD:
            context =  {
                'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE,
                'num_employers': num_companies,
                'EMPLOYER_THRESHOLD': settings.EMPLOYER_THRESHOLD
            }
        else:
            func_name = 'get_{}_plan'.format(benefit.lower())
            context = globals()[func_name](employers, num_companies)

        context['base_template'] = 'empty.html'
        context['today'] = today

        template = 'benefit/{}_plan.html'.format(benefit.lower())
        return render(request, template, context)
    elif benefit == 'EMPLOYERS':
        return render(request, 'benefit/employers.html', { 'today': today })
    return HttpResponse('Nice')


@csrf_exempt
def update_properties(request):
    form_param = request.POST
    benefit = form_param.get('benefit')
    plan = int(form_param.get('plan', 0))

    # save for print
    if plan != -1:
        request.session['plan'] = plan
    else:
        plan = request.session['plan']

    if benefit in PLAN_ALLOWED_BENEFITS:
        func_name = 'get_{}_properties'.format(benefit.lower())
        return globals()[func_name](request, plan)
    else:
        return HttpResponse('{}')


def get_life_properties(request, plan):
    context = {}
    multiple_max = 'N/A'
    flat_amount = 'N/A'
    multiple = 'N/A'
    add_flat = 'N/A'
    add_multiple = 'N/A'
    rank_flat = 'N/A'
    rank_multiple = 'N/A'

    if plan:
        employers, num_companies = get_filtered_employers_session(request)

        lifes = Life.objects.filter(employer__in=employers)
        life = Life.objects.get(id=plan)
        multiple_max = '${:,.0f}'.format(life.multiple_max) if life.multiple_max else 'N/A'
        flat_amount = '${:,.0f}'.format(life.flat_amount) if life.flat_amount else 'N/A'
        multiple = '{:03.1f}'.format(life.multiple) if life.multiple else 'N/A'
        
        if life.type == 'Flat Amount':
            add_flat = 'Yes' if life.add else 'No'
            if life.flat_amount:
                qs_flat_amount = lifes.exclude(flat_amount__isnull=True)
                quintile_array_flat = get_incremental_array(qs_flat_amount, 'flat_amount') 
                rank_flat = get_rank(quintile_array_flat, life.flat_amount)
        else:
            add_multiple = 'Yes' if life.add else 'No'
            if life.multiple_max:
                qs_multiple_max = lifes.exclude(multiple_max__isnull=True)
                quintile_array_multiple = get_incremental_array(qs_multiple_max, 'multiple_max') 
                rank_multiple = get_rank(quintile_array_multiple, life.multiple_max)

    context['multiple_max'] = multiple_max
    context['flat_amount'] = flat_amount
    context['multiple'] = multiple
    context['add_flat'] = add_flat
    context['add_multiple'] = add_multiple
    context['rank_flat'] = rank_flat
    context['rank_multiple'] = rank_multiple
    return JsonResponse(context, safe=False)


def get_std_properties(request, plan):
    context = {}
    weekly_max = 'N/A'
    percentage = 'N/A'
    salary_cont = 'N/A'
    duration_weeks = 'N/A'
    waiting_injury = 'N/A'
    waiting_illness = 'N/A'
    rank_weekly_max = 'N/A'
    rank_duration_weeks = 'N/A'

    if plan:
        employers, num_companies = get_filtered_employers_session(request)

        stds = STD.objects.filter(employer__in=employers)
        std = STD.objects.get(id=plan)
        weekly_max = '${:,.0f}'.format(std.weekly_max) if std.weekly_max else 'N/A'
        percentage = '{:,.0f}%'.format(std.percentage) if std.percentage else 'N/A'
        duration_weeks = '{:,.0f}'.format(std.duration_weeks) if std.duration_weeks else 'N/A'
        waiting_injury = '{:,.0f}'.format(std.waiting_days) if std.waiting_days else 'N/A'
        waiting_illness = '{:,.0f}'.format(std.waiting_days_sick) if std.waiting_days_sick else 'N/A'
        salary_cont = 'Yes' if std.salary_cont else 'No'
        
        qs_weekly_max = stds.exclude(weekly_max__isnull=True)
        qs_duration_weeks = stds.exclude(duration_weeks__isnull=True)
        quintile_weekly_max = get_incremental_array(qs_weekly_max, 'weekly_max') 
        quintile_duration_weeks = get_incremental_array(qs_duration_weeks, 'duration_weeks') 

        rank_weekly_max = get_rank(quintile_weekly_max, std.weekly_max)
        rank_duration_weeks = get_rank(quintile_duration_weeks, std.duration_weeks)

    context['weekly_max'] = weekly_max
    context['percentage'] = percentage
    context['duration_weeks'] = duration_weeks
    context['waiting_injury'] = waiting_injury
    context['waiting_illness'] = waiting_illness
    context['salary_cont'] = salary_cont
    context['rank_weekly_max'] = rank_weekly_max
    context['rank_duration_weeks'] = rank_duration_weeks
    return JsonResponse(context, safe=False)


def get_ltd_properties(request, plan):
    context = {}
    monthly_max = 'N/A'
    percentage = 'N/A'
    waiting_weeks = 'N/A'
    rank_monthly_max = 'N/A'
    rank_waiting_weeks = 'N/A'

    if plan:
        ft_industries = request.session['ft_industries']
        ft_head_counts = request.session['ft_head_counts']
        ft_other = request.session['ft_other']
        ft_regions = request.session['ft_regions']

        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)

        ltds = LTD.objects.filter(employer__in=employers)
        ltd = LTD.objects.get(id=plan)
        monthly_max = '${:,.0f}'.format(ltd.monthly_max) if ltd.monthly_max else 'N/A'
        percentage = '{:,.0f}%'.format(ltd.percentage) if ltd.percentage else 'N/A'
        waiting_weeks = '{:,.0f}'.format(ltd.waiting_weeks) if ltd.waiting_weeks else 'N/A'
        
        qs_monthly_max = ltds.exclude(monthly_max__isnull=True)
        qs_waiting_weeks = ltds.exclude(waiting_weeks__isnull=True)
        quintile_monthly_max = get_incremental_array(qs_monthly_max, 'monthly_max') 
        quintile_waiting_weeks = get_incremental_array(qs_waiting_weeks, 'waiting_weeks') 

        rank_monthly_max = get_rank(quintile_monthly_max, ltd.monthly_max)
        rank_waiting_weeks = get_rank(quintile_waiting_weeks, ltd.waiting_weeks)

    context['monthly_max'] = monthly_max
    context['percentage'] = percentage
    context['waiting_weeks'] = waiting_weeks
    context['rank_monthly_max'] = rank_monthly_max
    context['rank_waiting_weeks'] = rank_waiting_weeks
    return JsonResponse(context, safe=False)


def get_strategy_properties(request, plan):
    context = {}
    tobacco_surcharge_amount = 'N/A'
    tobacco_surcharge = 'N/A'
    spousal_surcharge_amount = 'N/A'
    spousal_surcharge = 'N/A'
    rank_spousal_surcharge = 'N/A'
    rank_tobacco_surcharge = 'N/A'

    if plan:
        ft_industries = request.session['ft_industries']
        ft_head_counts = request.session['ft_head_counts']
        ft_other = request.session['ft_other']
        ft_regions = request.session['ft_regions']

        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)

        instances = Strategy.objects.filter(employer__in=employers)
        instance = Strategy.objects.get(id=plan)

        spousal_surcharge_amount = '${:,.0f}'.format(instance.spousal_surcharge_amount) if instance.spousal_surcharge_amount else 'N/A'
        tobacco_surcharge_amount = '${:,.0f}'.format(instance.tobacco_surcharge_amount) if instance.tobacco_surcharge_amount else 'N/A'
        tobacco_surcharge = 'Yes' if instance.tobacco_surcharge else 'No'
        spousal_surcharge = 'Yes' if instance.spousal_surcharge else 'No'
        
        qs_spousal_surcharge_amount = instances.exclude(spousal_surcharge_amount__isnull=True)
        qs_tobacco_surcharge_amount = instances.exclude(tobacco_surcharge_amount__isnull=True)
        quintile_spousal_surcharge = get_incremental_array(qs_spousal_surcharge_amount, 'spousal_surcharge_amount') 
        quintile_tobacco_surcharge = get_incremental_array(qs_tobacco_surcharge_amount, 'tobacco_surcharge_amount') 

        rank_spousal_surcharge = get_rank(quintile_spousal_surcharge, instance.spousal_surcharge_amount)
        rank_tobacco_surcharge = get_rank(quintile_tobacco_surcharge, instance.tobacco_surcharge_amount)

    context['tobacco_surcharge_amount'] = tobacco_surcharge_amount
    context['tobacco_surcharge'] = tobacco_surcharge
    context['spousal_surcharge_amount'] = spousal_surcharge_amount
    context['spousal_surcharge'] = spousal_surcharge
    context['rank_spousal_surcharge'] = rank_spousal_surcharge
    context['rank_tobacco_surcharge'] = rank_tobacco_surcharge
    return JsonResponse(context, safe=False)


def get_vision_properties(request, plan):
    context = {}
    attrs = [item.name for item in Vision._meta.fields if item.name not in ['id', 'employer', 'title']]
    for attr in attrs:
        context[attr] = 'N/A'

    for attr in vision_quintile_attr:
        context['rank_'+attr] = 'N/A'

    if plan:
        employers, num_companies = get_filtered_employers_session(request)
        medians, var_local = get_vision_plan_(employers, num_companies)
        instance = Vision.objects.get(id=plan)

        for attr in attrs:
            val = getattr(instance, attr)
            context[attr] = val if val else 'N/A'

        for attr in vision_quintile_attr:            
            context['rank_'+attr] = get_rank(var_local['quintile_'+attr], getattr(instance, attr))

    return JsonResponse(context, safe=False)


def get_strategy_plan(employers, num_companies):
    attrs = ['tobacco_surcharge_amount', 'spousal_surcharge_amount']
    qs = Strategy.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)
    
    var_local = {}
    for attr in attrs:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

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


vision_quintile_attr = ['exam_copay',
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
    for attr in vision_quintile_attr:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)
    return medians, var_local


def get_rank(quintile_array, value):
    if not value:
        return 'N/A'

    x_vals = []
    for idx in range(len(quintile_array)-1):
        if quintile_array[idx][1] <= value and value <= quintile_array[idx+1][1]:
            x_vals.append(quintile_array[idx+1][0])

    x_mean = 0
    for item in x_vals:
        x_mean += item

    try:
        x_mean = x_mean * 1.0 / len(x_vals)
    except Exception as e:
        print quintile_array, value, '@@@@@@@'

    for idx in range(1, 6):
        if x_mean <= idx * 20:
            return idx

    return 'N/A'


def get_life_plan(employers, num_companies):
    attrs = ['multiple', 'multiple_max', 'flat_amount']
    qs = Life.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {        
        'prcnt_add_flat': get_percent_count_( qs.filter(add=True, type='Flat Amount'), qs.filter(type='Flat Amount')),
        'prcnt_add_multiple': get_percent_count_( qs.filter(add=True, type='Multiple of Salary'), qs.filter(type='Multiple of Salary'))
    }

    for attr in ['multiple_max', 'flat_amount']:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)


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


def get_std_plan(employers, num_companies):
    attrs = ['waiting_days', 'waiting_days_sick', 'weekly_max', 'percentage', 'duration_weeks']
    qs = STD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {
        'prcnt_salary_cont': qs.filter(salary_cont=True).count() * 100 / qs.count(),
    }

    for attr in ['weekly_max', 'duration_weeks']:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'std')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())


def get_ltd_plan(employers, num_companies):
    ltds = LTD.objects.filter(employer__in=employers)
    attrs = ['waiting_weeks', 'monthly_max', 'percentage']
    qs = LTD.objects.filter(employer__in=employers)
    medians, sub_qs = get_medians(qs, attrs, num_companies)

    var_local = {}
    for attr in ['waiting_weeks', 'monthly_max']:
        var_local['quintile_'+attr] = get_incremental_array(sub_qs['qs_'+attr], attr)

    # percentages for plans and cost share
    prcnt_plan_count = get_plan_percentages(employers, num_companies, 'ltd')
    prcnt_cost_share = get_plan_cost_share(qs)

    return dict(var_local.items() 
              + prcnt_cost_share.items() 
              + prcnt_plan_count.items()
              + medians.items())


@csrf_exempt
def get_num_employers(request):
    form_param = request.POST
    ft_industries = form_param.getlist('industry[]', ['*'])
    ft_head_counts = form_param.getlist('head_counts[]') or ['0-2000000']
    ft_other = form_param.getlist('others[]')
    ft_regions = form_param.getlist('regions[]')
    benefit = form_param.get('benefit')

    employers, num_companies = get_filtered_employers(ft_industries, 
                                                      ft_head_counts, 
                                                      ft_other,
                                                      ft_regions)
    return HttpResponse('{:,.0f}'.format(num_companies))


def get_median_count(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    try:
        if count % 2 == 1:
            return values[int(round(count/2))], count
        else:
            return sum(values[count/2-1:count/2+1])/2, count
    except Exception as e:
        print term, '@@@@@@@@@@'


def get_percent_count(qs, attr):
    qs1 = qs.filter(**{ attr: True })
    qs2 = qs.exclude(**{ '{}__isnull'.format(attr): True })
    return get_percent_count_(qs1, qs2)


def get_percent_count_(qs1, qs2):
    return qs1.count() * 100 / qs2.count()


def get_incremental_array(queryset, term):
    num_points = settings.MAX_POINTS
    num_elements = queryset.count()

    interval = num_elements / num_points + 1 #if num_elements > num_points else 1

    # limit number of points as MAX_POINTS
    result = []
    idx = 0
    idx_ = 0

    for item in queryset.order_by(term):
        if idx % interval == 0:
            # result.append([idx_, getattr(item, term)])
            result.append(getattr(item, term))            
            idx_ += 1
        idx += 1
        # store last maximum value
        if idx == num_elements:
            last_value = getattr(item, term)

    # format labels for 20%, 40% ..., 100%
    idx = 0
    factor = 20
    num_points = len(result)
    result_ = []
    label_o = 0

    for item in result:
        label_ = int(idx * 100 / num_points)
        if label_o < factor and factor <= label_:
            label_ = factor
            factor += 20 
        label = '{}%'.format(label_)
        # result_.append([label, item])
        result_.append([label_, item])
        label_o = label_
        idx += 1

    result_[-1] = [100, last_value]
    return result_


@csrf_exempt
def get_plans(request):
    benefit = request.POST.get('benefit')
    group = request.user.groups.first().name
    plans = []

    if benefit in PLAN_ALLOWED_BENEFITS:
        plans = get_plans_(benefit, group)

    return render(request, 'includes/plans.html', { 'plans': plans })


def get_plans_(benefit, group):
    model = MODEL_MAP[benefit]
    if group == 'bnchmrk':
        objects = model.objects.all()
    else:
        objects = model.objects.filter(employer__broker=group)

    if benefit == 'LIFE':
        return [
                   [item.id, '{} - {} - {}'.format(item.employer.name, item.type, item.title)]
                   for item in objects.order_by('employer__name', 'title')
               ]
    elif benefit in ['STD', 'LTD', 'VISION']:
        return [
                   [item.id, '{} - {}'.format(item.employer.name, item.title)]
                   for item in objects.order_by('employer__name', 'title')
               ]
    elif benefit in ['STRATEGY']:
        return [
                   [item.id, '{}'.format(item.employer.name)]
                   for item in objects.order_by('employer__name')
               ]


def contact_us(request):
    return render(request, 'contact_us.html')


def company(request):
    return render(request, 'company.html')    


def get_plan_percentages(employers, num_companies, attr):
    var_local = {}
    var_return = {}
    num_plans = 0

    for i in range(3):
        kwargs = { '{0}_count'.format(attr): i }
        var_local['num_plan{}'.format(i)] = employers.filter(**kwargs).count()
        num_plans += var_local['num_plan{}'.format(i)]
        var_return['prcnt_plan{}'.format(i)] = '{0:0.0f}'.format(var_local['num_plan{}'.format(i)] * 100.0 / num_companies)

    num_plan = num_companies - num_plans
    var_return['prcnt_plan3_or_more'] = '{0:0.0f}'.format(num_plan * 100.0 / num_companies)

    return var_return


def get_prevalence(qs, attr, val1, val2, keys):
    num_employers = len(qs.values_list('employer_id').distinct())       
    set1 = set([item.employer_id for item in qs.filter(**{ attr: val1 })])
    set2 = set([item.employer_id for item in qs.filter(**{ attr: val2 })])

    cnt_set1 = len(set1 - set2)
    cnt_set2 = len(set2 - set1)
    cnt_intersection = len(set2.intersection(set1))
    cnt_non_reported = num_employers - cnt_set1 - cnt_set2 - cnt_intersection

    return {
        keys[0]: '{0:0.0f}'.format(cnt_set1 * 100.0 / num_employers),
        keys[1]: '{0:0.0f}'.format(cnt_set2 * 100.0 / num_employers),
        keys[2]: '{0:0.0f}'.format(cnt_intersection * 100.0 / num_employers),
        keys[3]: '{0:0.0f}'.format(cnt_non_reported * 100.0 / num_employers)           
    }


def get_plan_cost_share(qs):
    keys = ['prcnt_paid', 'prcnt_share', 'prcnt_paid_share', 'prcnt_non_reported']
    return get_prevalence(qs, 'cost_share', '100% Employer Paid', 'Employee Cost Share', keys)


def get_plan_type(qs):
    keys = ['prcnt_type_plan_mul', 'prcnt_type_plan_flat', 'prcnt_type_plan_mul_flat', 'prcnt_type_non_reported']
    return get_prevalence(qs, 'type', 'Multiple of Salary', 'Flat Amount', keys)


def get_medians(qs, attrs, num_companies):
    var_local = {}
    var_return = {
        'EMPLOYER_THRESHOLD': settings.EMPLOYER_THRESHOLD,
        'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE,
        'num_employers': num_companies,    
    }

    for attr in attrs:
        kwargs = { '{0}__isnull'.format(attr): True }        
        var_local['qs_'+attr] = qs.exclude(**kwargs)
        mdn_attr, _ = get_median_count(var_local['qs_'+attr], attr)
        var_return['mdn_'+attr] = mdn_attr    

    return var_return, var_local


def get_filtered_employers_session(request):
    ft_industries = request.session['ft_industries']
    ft_head_counts = request.session['ft_head_counts']
    ft_other = request.session['ft_other']
    ft_regions = request.session['ft_regions']

    return get_filtered_employers(ft_industries, 
                                  ft_head_counts, 
                                  ft_other,
                                  ft_regions)
