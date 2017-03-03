import csv
import json
import collections

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('enterprise'))
        else:
            message = 'Your login credential is incorrect! Please try again.'
            return render(request, 'login.html', {
                'message': message,
            })


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login')) 


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

    return HttpResponse('Successfully imported!')


def import_life(request):
    path = '/home/akimmel/work/table extracts/life.csv'
    # path = '/root/work/Enterprise/data/life.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                life = Life.objects.create(                                                 
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
    return HttpResponse('Successfully imported!')


def import_std(request):
    path = '/home/akimmel/work/table extracts/STD.csv'    
    # path = '/root/work/Enterprise/data/STD.csv'

    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                std = STD.objects.create(                                                 
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

    return HttpResponse('Successfully imported!')


def get_filtered_employers(ft_industries, ft_head_counts, ft_other, ft_regions, lstart=0, lend=0, group='bnchmrk'):
    # filter with factors from UI (industry, head-count, other)
    q = Q()
    if not '*' in ft_industries:
        q = Q(industry1__in=ft_industries) | Q(industry2__in=ft_industries) | Q(industry3__in=ft_industries)

    for item in ft_other:
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
        num_companies = 0

    return employers, num_companies


@csrf_exempt
@login_required(login_url='/login')
def enterprise(request):
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
    form_param = request.POST
    ft_industries = form_param.getlist('industry[]', ['*'])
    ft_head_counts = form_param.getlist('head_counts[]') or ['0-2000000']
    ft_other = form_param.getlist('others[]')
    ft_regions = form_param.getlist('regions[]')
    benefit = form_param.get('benefit')
    request.session['benefit'] = benefit

    if benefit == 'HOME':
        full_name = '{} {}'.format(request.user.first_name, request.user.last_name)
        return render(request, 'home.html', locals())
    elif benefit == 'LIFE':
        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)
        return render(request, 'life_plan.html', get_life_plan(employers, num_companies))
    elif benefit == 'EMPLOYERS':
        return render(request, 'employers.html')
    return HttpResponse('Nice')


def get_life_plan(employers, num_companies):
    if num_companies == 0:
        return {
            'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE,
            'num_employers': num_companies,
        }

    lifes = Life.objects.filter(employer__in=employers)
    num_lifes = lifes.count()


    qs_multiple = lifes.exclude(multiple__isnull=True)
    mdn_multiple, cnt_multiple = get_median_count(qs_multiple, 'multiple')
    qs_multiple_max = lifes.exclude(multiple_max__isnull=True)
    mdn_multiple_max, cnt_multiple_max = get_median_count(qs_multiple_max, 'multiple_max')
    qs_flat_amount = lifes.exclude(flat_amount__isnull=True)
    mdn_flat_amount, cnt_flat_amount = get_median_count(qs_flat_amount, 'flat_amount')    
    mn_flat_amount, sdv_flat_amount = get_mean_sdv(qs_flat_amount, 'flat_amount')

    # for counting # of plans
    num_plan0 = employers.filter(life_count=0).count()
    num_plan1 = employers.filter(life_count=1).count()
    num_plan2 = employers.filter(life_count=2).count()
    num_plan3_or_more = num_companies - num_plan0 - num_plan1 - num_plan2

    prcnt_plan0 = '{0:0.1f}'.format(num_plan0 * 100.0 / num_companies)
    prcnt_plan1 = '{0:0.1f}'.format(num_plan1 * 100.0 / num_companies)
    prcnt_plan2 = '{0:0.1f}'.format(num_plan2 * 100.0 / num_companies)
    prcnt_plan3_or_more = '{0:0.1f}'.format(num_plan3_or_more * 100.0 / num_companies)

    flat_array = get_flat_array(qs_flat_amount) 
    flat_array_ = [['{0:0.1f}%'.format(item[1] * 100.0 / cnt_flat_amount), item[1]] for item in flat_array]
    flat_array = [[item[0], '{0:0.1f}'.format(item[1] * 100.0 / cnt_flat_amount)] for item in flat_array]
    flat_array.insert(0, ['0', 0.0]) # for formatting   

    cnt_add = lifes.filter(add=True).count()

    companies_with_mul_plan = set([item.employer_id for item in lifes.filter(type='Multiple of Salary')])
    companies_with_flat_plan = set([item.employer_id for item in lifes.filter(type='Flat Amount')])

    cnt_type_plan_none = num_plan0
    cnt_type_plan_mul = len(companies_with_mul_plan - companies_with_flat_plan)
    cnt_type_plan_flat = len(companies_with_flat_plan - companies_with_mul_plan)
    cnt_type_plan_mul_flat = len(companies_with_flat_plan.intersection(companies_with_mul_plan))
    cnt_type_non_reported = -(cnt_type_plan_mul_flat + cnt_type_plan_none + cnt_type_plan_mul + cnt_type_plan_flat - num_companies)

    companies_with_paid = set([item.employer_id for item in lifes.filter(cost_share='100% Employer Paid')])
    companies_with_share = set([item.employer_id for item in lifes.filter(cost_share='Employee Cost Share')])
    cnt_paid = len(companies_with_paid - companies_with_share)
    cnt_share = len(companies_with_share - companies_with_paid)
    cnt_paid_share = len(companies_with_share.intersection(companies_with_paid))
    cnt_non_reported = num_companies - num_plan0 - cnt_paid - cnt_share - cnt_paid_share

    prcnt_add = '{0:0.1f}%'.format(cnt_add * 100.0 / num_lifes)
    prcnt_type_plan_none = '{0:0.1f}'.format(cnt_type_plan_none * 100.0 / num_companies)
    prcnt_type_plan_mul = '{0:0.1f}'.format(cnt_type_plan_mul * 100.0 / num_companies)
    prcnt_type_plan_flat = '{0:0.1f}'.format(cnt_type_plan_flat * 100.0 / num_companies)
    prcnt_type_plan_mul_flat = '{0:0.1f}'.format(cnt_type_plan_mul_flat * 100.0 / num_companies)
    prcnt_type_non_reported = '{0:0.1f}'.format(cnt_type_non_reported * 100.0 / num_companies)

    prcnt_paid = '{0:0.1f}'.format(cnt_paid * 100.0 / num_companies)
    prcnt_share = '{0:0.1f}'.format(cnt_share * 100.0 / num_companies)
    prcnt_paid_share = '{0:0.1f}'.format(cnt_paid_share * 100.0 / num_companies)    
    prcnt_non_reported = '{0:0.1f}'.format(cnt_non_reported * 100.0 / num_companies)    

    return {
        'EMPLOYER_THRESHOLD_MESSAGE': settings.EMPLOYER_THRESHOLD_MESSAGE,
        'num_employers': num_companies,
        
        'mdn_multiple': mdn_multiple,
        'cnt_multiple': cnt_multiple,
        'mdn_multiple_max': mdn_multiple_max, 
        'cnt_multiple_max': cnt_multiple_max,
        'mdn_flat_amount': mdn_flat_amount, 
        'cnt_flat_amount': cnt_flat_amount,
        'mn_flat_amount': mn_flat_amount,
        'sdv_flat_amount': sdv_flat_amount,
        'flat_array': mark_safe(json.dumps(flat_array)),
        'flat_array_': flat_array_,
        
        'cnt_add': cnt_add,
        'cnt_type_plan_none': cnt_type_plan_none,
        'cnt_type_plan_mul': cnt_type_plan_mul,
        'cnt_type_plan_flat': cnt_type_plan_flat,
        'cnt_type_plan_mul_flat': cnt_type_plan_mul_flat,
        'cnt_type_non_reported': cnt_type_non_reported,
        'cnt_paid': cnt_paid,
        'cnt_share': cnt_share,
        'cnt_paid_share': cnt_paid_share,
        'cnt_non_reported': cnt_non_reported,
        
        'prcnt_add': prcnt_add,
        'prcnt_type_plan_none': prcnt_type_plan_none,
        'prcnt_type_plan_mul': prcnt_type_plan_mul,
        'prcnt_type_plan_flat': prcnt_type_plan_flat,
        'prcnt_type_plan_mul_flat': prcnt_type_plan_mul_flat,
        'prcnt_type_non_reported': prcnt_type_non_reported,
        'prcnt_paid': prcnt_paid,
        'prcnt_share': prcnt_share,
        'prcnt_paid_share': prcnt_paid_share,
        'prcnt_non_reported': prcnt_non_reported,
        
        'num_plan0': num_plan0,
        'num_plan1': num_plan1,
        'num_plan2': num_plan2,
        'num_plan3_or_more': num_plan3_or_more,

        'prcnt_plan0': prcnt_plan0,
        'prcnt_plan1': prcnt_plan1,
        'prcnt_plan2': prcnt_plan2,
        'prcnt_plan3_or_more': prcnt_plan3_or_more,
    }


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
    return HttpResponse(num_companies or "<25")


def get_median_count(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    if count % 2 == 1:
        return values[int(round(count/2))], count
    else:
        return sum(values[count/2-1:count/2+1])/2, count


def get_flat_array(lifes):
    min_ = settings.FLAT_BUCKET_SIZE
    max_ = 100000

    bucket_title = ['<$10k', '$20k', '$30k', '$40k', '$50k', '$60k', '$70k', '$80k', '$90k', '$100k', '$100k+']
    buckets = [[item, item+settings.FLAT_BUCKET_SIZE-1] for item in range(min_, max_-1, settings.FLAT_BUCKET_SIZE)]
    buckets.append([max_, 10000000])
    buckets.insert(0, [0, min_-1])

    f_array = []
    idx = 0
    for bucket in buckets:
        cnt = lifes.filter(flat_amount__gte=bucket[0], flat_amount__lte=bucket[1]).count()
        f_array.append([bucket_title[idx], cnt])
        idx += 1

    return f_array


def get_mean_sdv(queryset, term):
    mean = queryset.aggregate(Avg(term))
    sdv = queryset.aggregate(StdDev(term))
    return int(mean.values()[0]), int(sdv.values()[0])
