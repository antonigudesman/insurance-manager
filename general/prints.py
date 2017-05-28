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

import logging
log = logging.getLogger(__name__)

@login_required(login_url='/admin/login')
def print_template(request):
    p_benefit = json.loads(request.GET.get('p_benefit'))
    benefit = p_benefit['benefit']
    request.session['bnchmrk_benefit'] = benefit
    request.session['plan'] = p_benefit['plan']
    request.session['plan_type'] = p_benefit['plan_type']

    if 'quintile_properties' in p_benefit:
        request.session[benefit+'_quintile_properties'] = p_benefit['quintile_properties']
        request.session[benefit+'_quintile_properties_inv'] = p_benefit['quintile_properties_inv']
        request.session[benefit+'_services'] = p_benefit['services']  

    return get_response_template(request, 
                                 benefit, 
                                 True)


@login_required(login_url='/admin/login')
def print_template_header(request):
    p_benefit = json.loads(request.GET.get('p_benefit'))
    request.session['bnchmrk_benefit'] = p_benefit['benefit']
    request.session['plan'] = p_benefit['plan']
    request.session['plan_type'] = p_benefit['plan_type']

    return get_response_template(request, 
                                 p_benefit['benefit'], 
                                 True,
                                 True)


@login_required(login_url='/admin/login')
def print_page(request):
    return get_pdf(request, [{
        'benefit': request.session['bnchmrk_benefit'],
        'plan': request.session['plan'],
        'plan_type': request.session['plan_type'],
    }])


def get_pdf(request, print_benefits, download=True):
    # store original benefit and plan for front end
    benefit_o = request.session.get('bnchmrk_benefit')
    plan_o = request.session.get('plan')

    # get screenshot for current page with same session using selenium    
    driver = webdriver.PhantomJS()
    driver.set_window_size(1850, 1000)

    cc = { 
        'domain': request.META.get('HTTP_HOST').split(':')[0], 
        'name': 'sessionid', 
        'value': request.COOKIES.get('sessionid'), 
        'path': '/'
    }

    try:
        driver.add_cookie(cc)
    except Exception as e:
        pass

    # initialize pdf file
    page_height_on_image = 1240.0
    page_width_on_image = 1500
    margin_h = 90
    margin_v = ((page_width_on_image+2*margin_h) * 0.773 - page_height_on_image) / 2

    pdf = FPDF(orientation='L', format=(page_height_on_image+2*margin_v, page_width_on_image+2*margin_h), unit='pt')
    pdf.set_auto_page_break(False)

    base_path = '/tmp/page{}'.format(random.randint(-100000000, 100000000))
    pdf_path = base_path + '.pdf'

    try:
        vars_d = {}
        uidx = 0

        # for header
        url = 'http://{}/25Wfr7r2-3h4X25t?p_benefit={}'.format(request.META.get('HTTP_HOST'), 
            json.dumps(print_benefits[0]))
        print url, '######################3'
        driver.get(url)
        time.sleep(0.8)
        vars_d['img_path_header_{}'.format(uidx)] = '{}_{}_header.png'.format(base_path, uidx)
        driver.save_screenshot(vars_d['img_path_header_{}'.format(uidx)])
        
        # build a pdf with images using fpdf
        pdf.add_page()
        pdf.image(vars_d['img_path_header_{}'.format(uidx)], margin_h, margin_v)
        os.remove(vars_d['img_path_header_{}'.format(uidx)])

        for p_benefit in print_benefits:
            vars_d['img_path_{}'.format(uidx)] = '{}_{}.png'.format(base_path, uidx)

            # for body
            url = 'http://{}/98Wf37r2-3h4X2_jh9?p_benefit={}'.format(request.META.get('HTTP_HOST'), 
                json.dumps(p_benefit))

            print url, '#############3'
            driver.get(url)        
            time.sleep(1.6) #0.6
            # if benefits[uidx] in ['MEDICALRX']:
            #     time.sleep(1) #1.2

            driver.save_screenshot(vars_d['img_path_{}'.format(uidx)])

            # split the image in proper size
            origin = Image.open(vars_d['img_path_{}'.format(uidx)])
            header_height = 100
            bottom_height = 140
            width, height = origin.size

            num_pages = int(( height - header_height - bottom_height ) / page_height_on_image + 0.99)
            
            for idx in range(num_pages):
                vars_d['img_path_s_{}_{}'.format(uidx, idx)] = '{}_{}_{}s.png'.format(base_path, idx, uidx)
                height_s = header_height + page_height_on_image * (idx + 1) + 1
                if height_s > height - bottom_height:
                    height_s = height - bottom_height
                origin.crop((174,header_height+page_height_on_image*idx-1, 177+page_width_on_image, height_s+2)) \
                    .save(vars_d['img_path_s_{}_{}'.format(uidx, idx)])

                pdf.add_page()
                pdf.image(vars_d['img_path_s_{}_{}'.format(uidx, idx)], margin_h, margin_v)
                os.remove(vars_d['img_path_s_{}_{}'.format(uidx, idx)])
            # remove image files
            # os.remove(vars_d['img_path_{}'.format(uidx)])
            uidx += 1
    except Exception, e:
        # raise e
        log.debug(str(e))
        log.debug('###########32')


    pdf.output(pdf_path, "F")

    try:
        driver.quit()
    except Exception as e:
        pass
       
    # restore benefit and plan
    request.session['bnchmrk_benefit'] = benefit_o
    request.session['plan'] = plan_o                 

    if download:
        return get_download_response(pdf_path)    
    return pdf_path[5:]


@login_required(login_url='/admin/login')
def print_report_pdf(request, company_id):
    # company_id = request.GET.get('company_id')
    models = [Medical, Dental, Vision, Life, STD, LTD, Strategy]
    benefits = []
    plans = []
    plan_types = []

    for model in models:
        benefit = model.__name__.upper()
        instance = model.objects.filter(employer=company_id)
        for instance_ in instance:
            plan = instance_.id
            try:
                plan_type = getattr(instance_, 'type')
                if plan_type in ['PPO', 'POS']:
                    plan_type = 'PPO'
                elif plan_type in ['HMO', 'EPO']:
                    plan_type = 'HMO'
            except Exception as e:
                plan_type = None

            if benefit == 'MEDICAL':
                benefit = 'MEDICALRX'

            benefits.append(benefit)
            plans.append(plan)
            plan_types.append(plan_type)
    log.debug(benefits)
    # log.debug(plans)
    # log.debug('@@@@@@@@@@@2')
    return get_pdf(request, benefits, plans, plan_types)

@csrf_exempt
def print_report_in_order(request):
    print_order = json.loads(request.POST['print_order'])
    print print_order, '#########'
    file_path = get_pdf(request, print_order, False)
    return HttpResponse(file_path)

def download_report(request, report_name):
    base_path = '/tmp/'
    return get_download_response(base_path+report_name)    

def get_download_response(path):
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str( os.path.basename( path ) )
    return response
