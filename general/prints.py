import os
import time
import random
import mimetypes

from fpdf import FPDF
from PIL import Image

from django.core.files.storage import FileSystemStorage
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from wsgiref.util import FileWrapper
from selenium import webdriver

from .views import *


@login_required(login_url='/admin/login')
def print_template(request):
    benefit = request.GET.get('benefit')
    plan = request.GET.get('plan')
    #Retrieve data or whatever you need
    request.session['benefit'] = benefit
    request.session['plan'] = plan
    # Retrieve data or whatever you need
    ft_industries = request.session['ft_industries']
    ft_head_counts = request.session['ft_head_counts']
    ft_other = request.session['ft_other']
    ft_regions = request.session['ft_regions']

    ft_industries_label = 'All'
    ft_head_counts_label = 'All'
    ft_other_label = 'All'
    ft_regions_label = 'All'

    return get_response_template(request, 
                                 benefit, 
                                 ft_industries, 
                                 ft_head_counts, 
                                 ft_other, 
                                 ft_regions, 
                                 True,
                                 ft_industries_label,
                                 ft_head_counts_label,
                                 ft_other_label,
                                 ft_regions_label)


@login_required(login_url='/admin/login')
def print_template_header(request):
    benefit = request.GET.get('benefit')
    plan = request.GET.get('plan')
    #Retrieve data or whatever you need
    request.session['benefit'] = benefit
    request.session['plan'] = plan
    ft_industries = request.session['ft_industries']
    ft_head_counts = request.session['ft_head_counts']
    ft_other = request.session['ft_other']
    ft_regions = request.session['ft_regions']

    ft_industries_label = ', '.join(request.session['ft_industries_label'])
    ft_head_counts_label = ', '.join(request.session['ft_head_counts_label'])
    ft_other_label = ', '.join(request.session['ft_other_label'])
    ft_regions_label = ', '.join(request.session['ft_regions_label'])

    return get_response_template(request, 
                                 benefit, 
                                 ft_industries, 
                                 ft_head_counts, 
                                 ft_other, 
                                 ft_regions, 
                                 True,
                                 ft_industries_label,
                                 ft_head_counts_label,
                                 ft_other_label,
                                 ft_regions_label,
                                 True)


@login_required(login_url='/admin/login')
def print_page(request):
    # for universal format
    benefit = request.session['benefit']
    plan = request.session['plan']
    return get_pdf(request, [benefit], [plan])


def get_pdf(request, benefits, plans):
    # store original benefit and plan for front end
    benefit_o = request.session['benefit']
    plan_o = request.session['plan']    

    # get screenshot for current page with same session using selenium    
    driver = webdriver.PhantomJS()
    driver.set_window_size(1360, 1000)

    cc = { 
        'domain': request.META.get('HTTP_HOST'), 
        'name': 'sessionid', 
        'value': request.COOKIES.get('sessionid'), 
        'path': '/'
    }

    try:
        driver.add_cookie(cc)
    except Exception as e:
        pass

    # initialize pdf file
    margin_v = 30
    margin_h = 103
    pdf = FPDF(orientation='L', format=(1200+2*margin_v, 1425+2*margin_h), unit='pt')
    pdf.set_auto_page_break(False)

    base_path = '/tmp/page{}'.format(random.randint(-100000000, 100000000))
    pdf_path = base_path + '.pdf'

    vars_d = {}
    for uidx in range(len(benefits)):
        vars_d['img_path_{}'.format(uidx)] = '{}_{}.png'.format(base_path, uidx)
        vars_d['img_path_header_{}'.format(uidx)] = '{}_{}_header.png'.format(base_path, uidx)

        # for body
        url = 'http://{}/98Wf37r2-3h4X2_jh9?benefit={}&plan={}'.format(request.META.get('HTTP_HOST'), benefits[uidx], plans[uidx])
        print url, '@@@@@@@@@@@@'
        driver.get(url)        
        time.sleep(1)
        if benefits[uidx] in ['PPO', 'HDHP', 'HMO']:
            time.sleep(2)

        driver.save_screenshot(vars_d['img_path_{}'.format(uidx)])

        # for header
        url = 'http://{}/25Wfr7r2-3h4X25t?benefit={}&plan={}'.format(request.META.get('HTTP_HOST'), benefits[uidx], plans[uidx])
        print url, '@@@@@@@@@@@@'
        driver.get(url)
        time.sleep(1)
        driver.save_screenshot(vars_d['img_path_header_{}'.format(uidx)])
        
        # build a pdf with images using fpdf
        pdf.add_page()
        pdf.image(vars_d['img_path_header_{}'.format(uidx)], margin_h, margin_v)

        # split the image in proper size
        origin = Image.open(vars_d['img_path_{}'.format(uidx)])
        header_height = 141 - 5
        width, height = origin.size

        num_pages = int(( height - header_height ) / 1200.0 + 0.5)

        for idx in range(num_pages):
            vars_d['img_path_s_{}_{}'.format(uidx, idx)] = '{}_{}_{}s.png'.format(base_path, idx, uidx)
            height_s = header_height + 1200 * (idx + 1) + 1
            if height_s > height:
                height_s = height
            origin.crop((0,header_height+1200*idx, width, height_s)).save(vars_d['img_path_s_{}_{}'.format(uidx, idx)])

            pdf.add_page()
            pdf.image(vars_d['img_path_s_{}_{}'.format(uidx, idx)], margin_h, margin_v)
            os.remove(vars_d['img_path_s_{}_{}'.format(uidx, idx)])
        # remove image files
        os.remove(vars_d['img_path_{}'.format(uidx)])
        os.remove(vars_d['img_path_header_{}'.format(uidx)])

    pdf.output(pdf_path, "F")

    try:
        driver.quit()
    except Exception as e:
        pass
       
    # restore benefit and plan
    request.session['benefit'] = benefit_o
    request.session['plan'] = plan_o                 

    return get_download_response(pdf_path)    


@login_required(login_url='/admin/login')
def print_report(request):
    company_id = request.GET.get('company_id')
    models = [Medical, Dental, Vision, Life, STD, LTD, Strategy]

    benefits = []
    plans = []

    for model in models:
        benefit = model.__name__.upper()
        instance = model.objects.filter(employer=company_id)
        for instance_ in instance:
            plan = instance_.id
            try:
                type = getattr(instance_, 'type')
                if type in ['PPO', 'POS']:
                    benefit = 'PPO'
                elif type in ['HMO', 'EPO']:
                    benefit = 'HMO'
                elif type in ['HDHP', 'DPPO', 'DMO']:
                    benefit = type
            except Exception as e:
                pass

            benefits.append(benefit)
            plans.append(plan)
    # print benefits, plans
    return get_pdf(request, benefits, plans)


def get_download_response(path):
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str( os.path.basename( path ) )
    return response
