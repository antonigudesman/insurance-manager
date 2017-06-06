from django.conf import settings
from django.db.models import Q
from django.shortcuts import render

from .models import *
import pdb
import json

def get_filtered_employers(ft_industries, 
                           ft_head_counts, 
                           ft_other, 
                           ft_regions, 
                           ft_states,
                           lstart=0, 
                           lend=0, 
                           group='bnchmrk', 
                           q='',
                           threshold=1):
    # filter with factors from UI (industry, head-count, other)
    # filter for keyword
    q = Q(name__icontains=q)
    if not '*' in ft_industries:
        q = Q(industry1__in=ft_industries) | Q(industry2__in=ft_industries) | Q(industry3__in=ft_industries)

    # filter for others
    for item in ft_other:
        if item != '*':
            q &= Q(**{item: True})

    # filter for region
    q_region = Q()
    if not '*' in ft_regions:
        for item in ft_regions:
            q_region |= Q(**{item: True})
    q &= q_region

    # filter for head count
    q_ = Q(size=0)
    for ft_head_count in ft_head_counts:
        ft_vals = ft_head_count.split('-')        
        q_ |= Q(size__gte=int(ft_vals[0])) & Q(size__lte=int(ft_vals[1]))

    # filter for state
    if ft_states and not '*' in ft_states:
        q &= Q(state__in=ft_states)

    employers_ = Employer.objects.filter(q & q_).order_by('name')
    # for only accounts
    if group != "bnchmrk" and lend:
        employers_ = employers_.filter(broker=group)
    # else:
        # select = {'new_name':
        #     'CASE WHEN broker=\'Core\' THEN name WHEN broker=\'{}\' THEN name ELSE \'De-identified Employer\' END'.format(group)}
        # employers_ = Employer.objects.filter(q & q_).extra(select=select).order_by('new_name')
        
    employers = employers_
    num_companies = employers_.count()    
    
    if lend > 0:
        employers = employers_[lstart:lend]

    # filter with number of companies
    if num_companies < settings.EMPLOYER_THRESHOLD and threshold:
        employers = []
        # num_companies = 0

    return employers, num_companies


def get_filtered_employers_session(request):
    ft_industries = request.session.get('ft_industries', ['*'])
    ft_head_counts = request.session.get('ft_head_counts', ['0-2000000'])
    ft_other = request.session.get('ft_other', [])
    ft_regions = request.session.get('ft_regions', ['*'])
    ft_states = request.session.get('ft_states', [])

    return get_filtered_employers(ft_industries, 
                                  ft_head_counts, 
                                  ft_other,
                                  ft_regions,
                                  ft_states)


EXCEPT_ZERO_FIELDS = [
    'rx_ded_single',
    'rx_ded_family',
    'rx_max_single',
    'rx_max_family',
]

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
        if attr in EXCEPT_ZERO_FIELDS:       
            kwargs = { '{0}'.format(attr): 0 } 
            var_local['qs_'+attr] = var_local['qs_'+attr].exclude(**kwargs)

        mdn_attr, _ = get_median_count(var_local['qs_'+attr], attr)
        var_return['mdn_'+attr] = mdn_attr
        if mdn_attr != '-':
            var_return['mdn_'+attr] = '${:,.0f}'.format(mdn_attr)

    for attr in attrs_percent:
        kwargs = { '{0}__isnull'.format(attr): True }        
        var_local['qs_'+attr] = qs.exclude(**kwargs)
        mdn_attr, _ = get_median_count(var_local['qs_'+attr], attr)
        var_return['mdn_'+attr] = mdn_attr
        if mdn_attr != '-':
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
    return '-'


def get_median_count(queryset, term):
    count = queryset.count()
    values = queryset.values_list(term, flat=True).order_by(term)
    try:
        if count % 2 == 1:
            return values[int(round(count/2))], count
        else:
            return sum(values[count/2-1:count/2+1])/2, count
    except Exception as e:
        return '-', 0

def get_incremental_array(queryset, term, benefit=''):
    threshold_key = benefit + '__' + term

    # pdb.set_trace()
    if threshold_key in settings.QUINTILE_THRESHOLD:
        threshold = settings.QUINTILE_THRESHOLD[threshold_key]
        kwargs = { '{0}__gte'.format(term): threshold[0] }
        queryset = queryset.filter(**kwargs)
        kwargs = { '{0}__lte'.format(term): threshold[1] }
        queryset = queryset.filter(**kwargs)

    num_elements = queryset.count()
    raw_ya = [getattr(item, term) for item in queryset.order_by(term)]
    return get_incremental_array_(num_elements, raw_ya)


def get_incremental_array_(num_elements, raw_ya):
    # pdb.set_trace()
    result = []
    if raw_ya:
        for xa in range(0, 110, 10):
            y_idx = int(num_elements * xa * 1.0 / 100 + 0.5)
            if xa == 0:
                y_idx = int(num_elements * settings.MIN_PERCENTILE * 1.0 / 100 + 0.5)
            elif xa == 100:
                y_idx = int(num_elements * settings.MAX_PERCENTILE * 1.0 / 100 + 0.5)

            if y_idx == num_elements:
                y_idx -= 1
            result.append([xa, raw_ya[y_idx]])
    return result


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
    if value == None or value == '-' or quintile_array == []:
        return '-'

    # for specific filtering cases
    if quintile_array[0][1] > value:
        return settings.MIN_PERCENTILE;
    elif quintile_array[-1][1] < value:
        return settings.MAX_PERCENTILE;

    # get low index
    for idx in range(len(quintile_array)):
        if quintile_array[idx][1] >=  value:
            u_idx = idx
            break

    # get low index
    for idx in range(len(quintile_array)-1, -1, -1):
        if quintile_array[idx][1] <=  value:
            l_idx = idx
            break

    try:
        if l_idx == u_idx:
            percentile = min(quintile_array[l_idx][0], settings.MAX_PERCENTILE)
            percentile = max(percentile, settings.MIN_PERCENTILE)         
            return percentile
        if l_idx > u_idx:
            tt = u_idx
            u_idx = l_idx
            l_idx = tt
    except Exception as e:
        pdb.set_trace()

    # pdb.set_trace()
    xa = 0
    for idx in range(l_idx, u_idx+1):
        xa += quintile_array[idx][0]
    # try:
    xa = int(xa * 1.0 / (u_idx - l_idx + 1))
    # except Exception as e:
    # pdb.set_trace()

    ya = 0
    for idx in range(l_idx, u_idx+1):
        ya += quintile_array[idx][1]
    ya = ya * 1.0 / (u_idx - l_idx + 1)

    u_diff = quintile_array[u_idx][1] - value
    l_diff = value - quintile_array[l_idx][1]
    m_diff = abs(ya - value)

    if u_diff < l_diff and u_diff < m_diff:
        percentile = quintile_array[u_idx][0]
    elif l_diff < u_diff and l_diff < m_diff:
        percentile = quintile_array[l_idx][0]
    else:
        percentile = xa        

    percentile = min(percentile, settings.MAX_PERCENTILE)
    percentile = max(percentile, settings.MIN_PERCENTILE)            
    return percentile


def get_init_properties(attrs, rank_attrs):
    context = {}

    for attr in attrs:
        context[attr] = ''

    for attr in rank_attrs:
        context['rank_'+attr] = ''

    return context


def get_dollar_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = '-'
        if val != None:
            context[attr] = '${:,.0f}'.format(val)


def get_percent_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = '{:,.0f}%'.format(val) if val != None else '-'


def get_int_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = val if val != None else '-'


def get_float_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        context[attr] = '{:03.1f}'.format(val) if val != None else '-'


def get_boolean_properties(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        if val != None:
            context[attr] = 'Yes' if val else 'No'
        else:
            context[attr] = '-'


def get_boolean_properties_5_states(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        if val != None:
            context[attr] = 'Yes' if val in ['TRUE', 'True/Coin'] else 'No'
        else:
            context[attr] = '-'


def get_boolean_properties_5_states_coin(instance, attrs, context):
    for attr in attrs:
        val = getattr(instance, attr)
        if val != None:
            context['coin_'+attr] = 'Yes' if val in ['False/Coin', 'True/Coin'] else 'No'
        else:
            context['coin_'+attr] = '-'


def get_quintile_properties(var_qs, instance, attrs, attrs_inv, context):
    for attr in attrs:            
        context['rank_'+attr] = get_rank(var_qs['quintile_'+attr], getattr(instance, attr))

    for attr in attrs_inv: 
        rank = get_rank(var_qs['quintile_'+attr], getattr(instance, attr))
        rank = rank if rank == '-' else 100 - rank
        context['rank_'+attr] = rank if rank != 100 else settings.MAX_PERCENTILE


def get_quintile_properties_idx(var_qs, instance, attrs, attrs_inv, context):
    idx = 0
    for attr in attrs:            
        context['rank_'+attr] = get_rank(var_qs['quintile_'+str(idx)], getattr(instance, attr))
        idx += 1

    for attr in attrs_inv: 
        rank = get_rank(var_qs['quintile_'+str(idx)], getattr(instance, attr))
        rank = rank if rank == '-' else 100 - rank
        context['rank_'+attr] = rank if rank != 100 else settings.MAX_PERCENTILE
        idx += 1


def get_industries():
    # get valid distinct industries 
    industries1 = Employer.objects.order_by('industry1').values_list('industry1').distinct()
    industries1 = [item[0] for item in industries1 if item[0]]
    industries2 = Employer.objects.order_by('industry2').values_list('industry2').distinct()
    industries2 = [item[0] for item in industries2 if item[0]]
    industries3 = Employer.objects.order_by('industry3').values_list('industry3').distinct()
    industries3 = [item[0] for item in industries3 if item[0]]
    return sorted(set(industries1 + industries2 + industries3))


def employee_pricing_medical(plans, service):
    detail = settings.CPT_COST[service]
    e_costs = []
    e_stacks = []

    for instance in plans:
        # for service, detail in settings.CPT_COST.items():
            attr = service.lower() + '_ded_apply'
            _apply = getattr(instance, attr)
            ded_max = getattr(instance, 'in_max_single')

            if _apply == None:
                # employee_cost = 0
                ded_cost = 0
                coin_cost = 0
                copay_cost = 0
            elif _apply == 'FALSE':
                ded_cost = 0
                coin_cost = 0
                copay_cost = getattr(instance, service.lower()+'_copay') or 0
            elif _apply == 'False/Coin':
                ded_cost = 0
                coin_cost = getattr(instance, 'in_coin') or 0
                copay_cost = 0
            elif _apply == 'TRUE':
                ded_cost = getattr(instance, 'in_ded_single') or 0
                coin_cost = 0
                copay_cost = getattr(instance, service.lower()+'_copay') or 0
            elif _apply == 'True/Coin':
                ded_cost = getattr(instance, 'in_ded_single') or 0
                coin_cost = getattr(instance, 'in_coin') or 0
                copay_cost = 0

            # print service, detail['value'], ded_max, '@@@@@@@@@@@@@@@@@@'
            # print _apply, ded_cost, coin_cost, copay_cost

            if ded_cost > detail['value']:
                coin_cost = 0
                employee_cost = detail['value']
            else:
                coin_cost *= (detail['value'] - ded_cost) * 1.0 / 100
                employee_cost = min(min(ded_max, int(ded_cost+coin_cost+copay_cost+0.5)), detail['value'])

            # print coin_cost
            # print employee_cost, '=================\n\n'
            if _apply:
                e_costs.append(employee_cost)
                e_stacks.append(['instance', detail['value'], ded_cost, coin_cost, copay_cost, _apply])

    return e_costs, e_stacks


def get_index(llist, val):
    for ii in range(len(llist)):
        if llist[ii] == val:
            return ii


def get_median_list(llist):
    s_llist = sorted(llist)
    idx = int(len(s_llist) * 1.0 / 2 - 0.5)
    val = s_llist[idx]
    return val, get_index(llist, val)


def encode_url(obj):
    return json.dumps(obj).replace('&', '$$$')


def decode_url(obj_str):
    return json.loads(obj_str.replace('$$$', '&'))