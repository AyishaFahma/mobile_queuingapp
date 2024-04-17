"""
URL configuration for QueuingApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('login/',views.login),
    path('login_post/',views.login_post),

    path('changepass/', views.changepass),
    path('changepass_post/',views.changepass_post),

    path('forget_password/',views.forget_password),
    path('forget_password_post/',views.forget_password_post),

    path('viewbusinesapprorej/', views.viewbusinesapprorej),
    path('viewbusinesapprorej_post/',views.viewbusinesapprorej_post),

    path('approve/<id>',views.approve),
    path('reject/<id>',views.reject),

    path('viewapprobusines/',views.viewapprobusines),
    path('viewapprobusines_post/',views.viewapprobusines_post),

    path('viewrejectbusines/',views.viewrejectbusines),
    path('viewrejectbusines_post/',views.viewrejectbusines_post),

    path('viewuser/',views.viewuser),
    path('viewuser_post/',views.viewuser_post),

    path('sendnotifi/',views.sendnotifi),
    path('sendnotifi_post/',views.sendnotifi_post),

    path('viewfeedapp/',views.viewfeedapp),
    path('viewfeedapp_post/',views.viewfeedapp_post),

    path('viewfeedbusines/',views.viewfeedbusines),
    path('viewfeedbusines_post/',views.viewfeedbusines_post),

    path('viewfeedfrmbusines/',views.viewfeedfrmbusines),
    path('viewfeedfrmbusines_post/',views.viewfeedfrmbusines_post),

    path('adminhome/',views.adminhome),

    path('signup/',views.signup),
    path('signup_post/',views.signup_post),

    path('changepassbussi/', views.changepassbussi),
    path('changepassbussi_post/',views.changepassbussi_post),

    path('viewprofile/',views.viewprofile),

    path('editprofile/',views.editprofile),
    path('editprofile_post/',views.editprofile_post),

    path('addslot/',views.addslot),
    path('addslot_post/',views.addslot_post),

    path('viewslot/',views.viewslot),
    path('deleteslot/<id>',views.deleteslot),

    path('confirmslotreq/',views.confirmslotreq),
    path('confirmslotreq_post/',views.confirmslotreq_post),

    path('approveslot/<id>',views.approveslot),
    path('rejectslot/<id>', views.rejectslot),

    path('viewapproslot/',views.viewapproslot),
    path('viewapproslot_post/',views.viewapproslot_post),

    path('viewrejectslot/',views.viewrejectslot),
    path('viewrejectslot_post/',views.viewrejectslot_post),

    path('sendnotifibusines/<id>',views.sendnotifibusines),
    path('sendnotifibusines_post/',views.sendnotifibusines_post),

    path('bussinesshome/',views.bussinesshome),

    path('viewnotifi/', views.viewnotifi),
    path('viewnotifi_post/',views.viewnotifi_post),

    path('deletenotifi/<id>',views.deletenotifi),

    path('sendfeed/',views.sendfeed),
    path('sendfeed_post/',views.sendfeed_post),





    path('user_login/',views.user_login),

    path('user_changepassword/',views.user_changepassword),

    path('user_signup/',views.user_signup),

    path('user_editprofile/',views.user_editprofile),

    path('user_viewprofile/',views.user_viewprofile),

    path('user_viewbussiness/',views.user_viewbussiness),

    path('user_viewbussiness_location/',views.user_viewbussiness_location),

    path('user_viewbussiness_byname/',views.user_viewbussiness_byname),

    path('user_viewcurrentslot/',views.user_viewcurrentslot),

    path('user_bookslot/',views.user_bookslot),

    path('user_viewestimated_waittime/',views.user_viewestimated_waittime),

    path('user_viewrealtime_updation/',views.user_viewrealtime_updation),

    path('user_view_notification/',views.user_view_notification),

    path('user_chat/',views.user_chat),

    path('user_feedbackbussiness/',views.user_feedbackbussiness),

    path('user_feedbackapp/',views.user_feedbackapp),
    path('user_view_request/',views.user_view_request),
    path('user_view_request_home/',views.user_view_request_home),
    path('business_updatestatus/<sid>',views.finish_booking),
    path('cancel_request/',views.cancel_slot),
    path('user_sendchat/',views.user_sendchat),
    path('user_viewchat/',views.user_viewchat),
    path('chat/<id>',views.chat),
    path('chat_view/',views.chat_view),
    path('chat_send/<msg>',views.chat_send),
    path('viewNotification/', views.viewNotification),

]
