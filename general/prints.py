import os
import time
import random
import HTMLParser
import mimetypes

from fpdf import FPDF
from PIL import Image
from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.utils.encoding import smart_str
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from wsgiref.util import FileWrapper
from selenium import webdriver

from .views import *


@login_required(login_url='/login')
def print_template(request):
    #Retrieve data or whatever you need
    benefit = request.session['benefit']
    ft_industries = request.session['ft_industries']
    ft_head_counts = request.session['ft_head_counts']
    ft_other = request.session['ft_other']
    ft_regions = request.session['ft_regions']

    ft_industries_label = ', '.join(request.session['ft_industries_label'])
    ft_head_counts_label = ', '.join(request.session['ft_head_counts_label'])
    ft_other_label = ', '.join(request.session['ft_other_label'])
    ft_regions_label = ', '.join(request.session['ft_regions_label'])

    if benefit == 'HOME':
        full_name = '{} {}'.format(request.user.first_name, request.user.last_name)
        return render(request, 'home.html', locals())
    elif benefit == 'LIFE':
        employers, num_companies = get_filtered_employers(ft_industries, 
                                                          ft_head_counts, 
                                                          ft_other,
                                                          ft_regions)

        context = get_life_plan(employers, num_companies)
        context['base_template'] = 'print.html'
        context['today'] = datetime.strftime(datetime.now(), '%B %d, %Y')
        # unescape html characters
        h = HTMLParser.HTMLParser()
        context['ft_industries_label'] = h.unescape(ft_industries_label)
        context['ft_head_counts_label'] = h.unescape(ft_head_counts_label)
        context['ft_other_label'] = h.unescape(ft_other_label)
        context['ft_regions_label'] = h.unescape(ft_regions_label)
        return render(request, 'life_plan.html', context)


@login_required(login_url='/login')
def print_page(request):
    # get screenshot for current page with same session using selenium    
    driver = webdriver.PhantomJS()
    driver.set_window_size(1360, 1000)

    cc = { 
        'domain': 'localhost', 
        'name': 'sessionid', 
        'value': request.COOKIES.get('sessionid'), 
        'path': '/'
    }

    try:
        driver.add_cookie(cc)
    except Exception as e:
        pass

    driver.get('http://{}/98Wf37r2-3h4X2_jh9'.format(request.META.get('HTTP_HOST')))
    base_path = '/tmp/page{}'.format(random.randint(-100000000, 100000000))
    img_path = base_path + '.png'
    pdf_path = base_path + '.pdf'
    time.sleep(2)

    driver.save_screenshot(img_path)
    driver.quit()

    # convert png into pdf using fpdf
    margin = 20
    width, height = Image.open(img_path).size

    pdf = FPDF(unit="pt", format=[width+2*margin, height+2*margin])
    pdf.add_page()

    pdf.image(img_path, margin, margin)

    pdf.output(pdf_path, "F")
    os.remove(img_path)
    return get_download_response(pdf_path)


def get_download_response(path):
    wrapper = FileWrapper( open( path, "r" ) )
    content_type = mimetypes.guess_type( path )[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Length'] = os.path.getsize( path ) # not FileField instance
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str( os.path.basename( path ) )
    return response
