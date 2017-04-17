import json
import HTMLParser
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from django.conf import settings


from .models import *
from .benefits import *

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
    'VISION': Vision,
    'DENTAL': Dental,
    'MEDICAL': Medical,
    'EMPLOYERS': Employer
}

PLAN_ALLOWED_BENEFITS = ['LIFE', 'STD', 'LTD', 'STRATEGY', 'VISION', 'DENTAL', 'MEDICAL']


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

    return get_response_template(request, benefit, ft_industries, ft_head_counts, ft_other, ft_regions)


def get_response_template(request, 
                          benefit, 
                          ft_industries, 
                          ft_head_counts, 
                          ft_other, 
                          ft_regions, 
                          is_print=False, 
                          ft_industries_label='', 
                          ft_head_counts_label='', 
                          ft_other_label='', 
                          ft_regions_label='',
                          is_print_header=False):

    today = datetime.strftime(datetime.now(), '%B %d, %Y')

    if benefit == 'HOME':
        full_name = '{} {}'.format(request.user.first_name, request.user.last_name)
        return render(request, 'benefit/home.html', locals())
    elif benefit in ['LIFE', 'STD', 'LTD', 'STRATEGY', 'VISION', 'DPPO', 'DMO', 'PPO', 'HMO', 'HDHP']:
        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)
        
        benefit_= None
        if benefit in ['DPPO', 'DMO']:
            benefit_ = benefit      # store original benefit
            benefit = 'DENTAL'
        elif benefit in ['PPO', 'HMO', 'HDHP']:
            benefit_ = benefit      # store original benefit
            benefit = 'MEDICAL'

        if num_companies < settings.EMPLOYER_THRESHOLD:
            context =  {
                'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE,
                'num_employers': num_companies,
                'EMPLOYER_THRESHOLD': settings.EMPLOYER_THRESHOLD
            }
        else:
            func_name = 'get_{}_plan'.format(benefit.lower())
            context = globals()[func_name](employers, num_companies, benefit_)

        context['base_template'] = 'print.html' if is_print else 'empty.html'
        context['today'] = today

        if is_print:
            # unescape html characters
            h = HTMLParser.HTMLParser()
            context['ft_industries_label'] = h.unescape(ft_industries_label)
            context['ft_head_counts_label'] = h.unescape(ft_head_counts_label)
            context['ft_other_label'] = h.unescape(ft_other_label)
            context['ft_regions_label'] = h.unescape(ft_regions_label)

        template = 'benefit/{}_plan.html'.format(benefit.lower())
        if is_print_header:
            group = request.user.groups.first().name
            context['group'] = group.lower()
            template = 'includes/print_header.html'

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

    benefit_= None
    if benefit in ['DPPO', 'DMO']:
        benefit_ = benefit      # store original benefit
        benefit = 'DENTAL'
    elif benefit in ['PPO', 'HMO', 'HDHP']:
        benefit_ = benefit      # store original benefit
        benefit = 'MEDICAL'

    if benefit in PLAN_ALLOWED_BENEFITS:
        func_name = 'get_{}_properties'.format(benefit.lower())
        return globals()[func_name](request, plan, benefit_)
    else:
        return HttpResponse('{}')


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


@csrf_exempt
def get_plans(request):
    benefit = request.POST.get('benefit')
    group = request.user.groups.first().name
    plans = []

    benefit_= None
    if benefit in ['DPPO', 'DMO']:
        benefit_ = benefit      # store original benefit
        benefit = 'DENTAL'
    elif benefit in ['PPO', 'HMO', 'HDHP']:
        benefit_ = benefit      # store original benefit
        benefit = 'MEDICAL'

    if benefit in PLAN_ALLOWED_BENEFITS + ['EMPLOYERS']:
        plans = get_plans_(benefit, group, benefit_)

    return render(request, 'includes/plans.html', { 'plans': plans })


def get_plans_(benefit, group, benefit_):
    model = MODEL_MAP[benefit]
    if group == 'bnchmrk':
        objects = model.objects.all()
    else:
        if benefit == 'EMPLOYERS':
            objects = model.objects.filter(broker=group)
        else:
            objects = model.objects.filter(employer__broker=group)

    if benefit_ in ['DPPO', 'DMO']:     # for DPPO, DMO pages
        objects = objects.filter(type=benefit_)
    elif benefit_ == 'PPO':
        objects = objects.filter(type__in=['PPO', 'POS'])
    elif benefit_ == 'HDHP':
        objects = objects.filter(type='HDHP')
    elif benefit_ == 'HMO':
        objects = objects.filter(type__in=['HMO', 'EPO'])

    if benefit in ['LIFE', 'DENTAL', 'MEDICAL']:
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
    elif benefit in ['EMPLOYERS']:
        return [
                   [item.id, '{}'.format(item.name)]
                   for item in objects.order_by('name')
               ]

def contact_us(request):
    return render(request, 'contact_us.html')


def company(request):
    return render(request, 'company.html')    
