from __future__ import unicode_literals

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views.i18n import set_language

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

from general.auth import *
from general.views import *
from general.prints import *
from general.imports import *

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

urlpatterns = i18n_patterns(
    # Change the admin prefix here to use an alternate URL for the
    # admin interface, which would be marginally more secure.
    url("^admin/", include(admin.site.urls)),
)

if settings.USE_MODELTRANSLATION:
    urlpatterns += [
        url('^i18n/$', set_language, name='set_language'),
    ]

urlpatterns += [
    url(r"^$", home, name="home"),
    url(r"^accounts$", accounts, name="accounts"),
    url(r"^accounts/(?P<id>.*)", account_detail, name="account_detail"),
    url(r"^account_detail_benefit$", account_detail_benefit, name="account_detail_benefit"),
    url(r"^update_benefit/(?P<instance_id>.*)$", update_benefit, name="update_benefit"),    

    url(r"^benchmarking/(?P<benefit>.*)$", benchmarking, name="benchmarking"),
    url(r"^_benchmarking", ajax_benchmarking, name="_benchmarking"),
    url(r"^get_plan_type", get_plan_type, name="get_plan_type"),
    url(r"^update_quintile", update_quintile, name="update_quintile"),
    url(r"^update_e_cost", update_e_cost, name="update_e_cost"),
    
    url(r"^support", support, name="support"),
    url(r"^faq$", faq, name="faq"),
    url(r"^faqs/(?P<id>\d+)", faq_detail, name="faq_detail"),

    # url("^", include("mezzanine.urls")),
    # authentication
    url(r"^login", user_login, name="login"),
    url(r"^logout", user_logout, name="logout"),
    url(r"^reset_password", reset_password, name="reset_password"),
    url(r"^change_password", change_password, name="change_password"),
    # main logic
    url(r"^enterprise", enterprise, name="enterprise"), # benchmarking
    # url(r"^_enterprise", ajax_enterprise, name="_enterprise"),
    url(r"^get_num_employers", get_num_employers, name="get_num_employers"),
    url(r"^get_plans", get_plans, name="get_plans"),
    url(r"^update_properties", update_properties, name="update_properties"),  

    # url(r"^import_employer", import_employer, name="import_employer"),
    # url(r"^import_life", import_life, name="import_life"),
    # url(r"^import_std", import_std, name="import_std"),
    # url(r"^import_ltd", import_ltd, name="import_ltd"),
    # url(r"^import_strategy", import_strategy, name="import_strategy"),
    # url(r"^import_vision", import_vision, name="import_vision"),    
    # url(r"^import_dental", import_dental, name="import_dental"),
    # url(r"^import_medical", import_medical, name="import_medical"),            
    
    # print page
    url(r"^98Wf37r2-3h4X2_jh9$", print_template, name="print_template"),
    url(r"^25Wfr7r2-3h4X25t$", print_template_header, name="print_template_header"),
    url(r"^print_page$", print_page, name="print_page"),
    url(r"^print_report$", print_report, name="print_report"),
    url(r"^print_history$", print_history, name="print_history"),
    url(r"^print_page_preview$", print_page_preview, name="print_page_preview"),
    url(r"^print_history/(?P<id>\d+)$", edit_print_history, name="edit_print_history"),
    url(r"^print_plan_order/(?P<company_id>.*)$", print_plan_order, name="print_plan_order"),
    url(r"^print_report_in_order$", print_report_in_order, name="print_report_in_order"),
    url(r"^print_contents$", print_contents, name="print_contents"),
    url(r"^download_report/(?P<report_name>.*)$", download_report, name="download_report"),
]

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
