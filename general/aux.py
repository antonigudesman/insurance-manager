from django.conf import settings
from django.db.models import Q

from .models import *

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


def get_filtered_employers_session(request):
    ft_industries = request.session['ft_industries']
    ft_head_counts = request.session['ft_head_counts']
    ft_other = request.session['ft_other']
    ft_regions = request.session['ft_regions']

    return get_filtered_employers(ft_industries, 
                                  ft_head_counts, 
                                  ft_other,
                                  ft_regions)


def get_medians(qs, attrs, num_companies, attrs_percent=[], attrs_int=[]):
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
        if mdn_attr != 'N/A':
            var_return['mdn_'+attr] = '${:,.0f}'.format(mdn_attr)

    for attr in attrs_percent:
        kwargs = { '{0}__isnull'.format(attr): True }        
        var_local['qs_'+attr] = qs.exclude(**kwargs)
        mdn_attr, _ = get_median_count(var_local['qs_'+attr], attr)
        var_return['mdn_'+attr] = mdn_attr
        if mdn_attr != 'N/A':
            var_return['mdn_'+attr] = '{:,.0f}%'.format(mdn_attr)

    for attr in attrs_int:
        kwargs = { '{0}__isnull'.format(attr): True }        
        var_local['qs_'+attr] = qs.exclude(**kwargs)
        mdn_attr, _ = get_median_count(var_local['qs_'+attr], attr)
        var_return['mdn_'+attr] = mdn_attr

    return var_return, var_local


def get_percent_count(qs, attr):
    qs1 = qs.filter(**{ attr: True })
    qs2 = qs.exclude(**{ '{}__isnull'.format(attr): True })
    return get_percent_count_(qs1, qs2)


def get_percent_count_(qs1, qs2):
    """
    Calculate percentageof a queryset over another one
    Return formatted percentage
    """
    cnt = qs2.count()
    if cnt:
        return '{:,.0f}%'.format(qs1.count() * 100 / cnt)
    return 'N/A'


def get_median_count(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    try:
        if count % 2 == 1:
            return values[int(round(count/2))], count
        else:
            return sum(values[count/2-1:count/2+1])/2, count
    except Exception as e:
        return 'N/A', 0

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

    if result_:
        result_[-1] = [100, last_value]
    return result_


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


def get_rank(quintile_array, value):
    if value == None or value == 'N/A':
        return 'N/A'

    # for specific filtering cases
    if quintile_array[0][1] > value:
        return 1;
    elif quintile_array[-1][1] < value:
        return 5;

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


def get_init_properties(attrs, rank_attrs):
    context = {}

    for attr in attrs:
        context[attr] = 'N/A'

    for attr in rank_attrs:
        context['rank_'+attr] = 'N/A'

    return context


def get_dollar_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = 'N/A'
        if val != None:
            context[attr] = '${:,.0f}'.format(val)


def get_percent_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = '{:,.0f}%'.format(val) if val != None else 'N/A'


def get_int_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = val if val != None else 'N/A'


def get_float_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = '{:03.1f}'.format(val) if val != None else 'N/A'


def get_boolean_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        if val != None:
            context[attr] = 'Yes' if val else 'No'
        else:
            context[attr] = 'N/A'


def get_quintile_properties(var_qs, instance, attrs, attrs_inv, context):
    for attr in attrs:            
        context['rank_'+attr] = get_rank(var_qs['quintile_'+attr], getattr(instance, attr))

    for attr in attrs_inv: 
        rank = get_rank(var_qs['quintile_'+attr], getattr(instance, attr))
        context['rank_'+attr] = rank if rank == 'N/A' else 6 - rank

