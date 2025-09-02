from django.urls import re_path,path
from django.conf.urls import include 
from django.conf import settings

from job_app.views.application import ApplicationView
from job_app.views.job import JobView
from job_app.views.skill import SkillView
from job_app.views.user import UserView
from .views.login import LoginViewSet
from .views.forget_password import ForgotPasswordView
from .views.verify_otp import VerifyPasswordView
from .views.reset_password import ResetPasswordView
from .views.logout import LogoutView
from .views.user_impersonate import ImpersonateView
from .views.login_verify_otp import LoginVerifyView

""" User login/ add/ logout profile urls"""
urlpatterns = [
    re_path(r'^login/$', LoginViewSet.as_view()),
    re_path(r'^logout/$', LogoutView.as_view()),
]

""" User forget_password/ verify_otp/ reset_password/ profile urls"""
urlpatterns += [
    re_path(r'^forget_password/$', ForgotPasswordView.as_view()),
    re_path(r'^verify_otp/$', VerifyPasswordView.as_view()),
    re_path(r'^reset_password/$', ResetPasswordView.as_view()),
]

""" User impersonate"""
urlpatterns += [
    re_path(r'^user-impersonate/(?P<id>.+)/$', ImpersonateView.as_view({'get': 'retrieve'})),
]

""" login-verify-otp"""
urlpatterns += [
    re_path(r'^login-verify-otp/$', LoginVerifyView.as_view({'get': 'retrieve'})),
]

        

from .views.student import StudentView

''' Student '''
urlpatterns += [
    re_path(r'^student/$', StudentView.as_view({'get': 'list', 'post': 'create', 'put': 'partial_update', 'delete': 'bulk_delete'})),
    re_path(r'^student/(?P<id>.+)/$', StudentView.as_view({'get': 'retrieve', 'delete': 'delete'})),
]


from .views.products import ProductsView

''' Products '''
urlpatterns += [
    re_path(r'^products/$', ProductsView.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^products/(?P<id>.+)/$', ProductsView.as_view({'get': 'retrieve' , 'put': 'partial_update', 'delete': 'bulk_delete', 'delete': 'delete'})),
]
           
'''Job Portal'''
urlpatterns += [
    # User endpoints    
    path('users/', UserView.as_view({'post': 'create', 'get': 'list'})),
    path('users/<int:id>/', UserView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'delete'})),

    # Job endpoints
    path('jobs/', JobView.as_view({'get': 'list', 'post': 'create'})),
    path('jobs/<int:id>/', JobView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'delete'})),

    # Application endpoints
    path('applications/', ApplicationView.as_view({'get': 'list', 'post': 'create'})),
    path('applications/<int:id>/', ApplicationView.as_view({'delete': 'delete', 'put': 'update'})),
    path('applications/<int:id>/update-status/', ApplicationView.as_view({'patch': 'update_status'})),

    #Skill endpoints
    path('skill/', SkillView.as_view({'get': 'list', 'post': 'create'}), name='skill-list-create'),
]