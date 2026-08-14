from django.urls import path

from .views import *


urlpatterns = [

    path( "dashboard/",dashboard,name="dashboard"),
    path("agencydashboard/",agencydashboard,name="agencydashboard"),
    path("admindashboard/",admindashboard,name="admindashboard"),
    path("updaterole/<int:id>/",update_role,name="update_role"),
    path("users/", user_list, name="user_list"),
    path("agencies/", agency_list, name="agency_list"),
   path("bookings/", booking_list, name="booking_list"),
   path("categories/", category_list, name="category_list"),
   path("reports/", reports, name="reports"),
   path("settings/", settings, name="settings"),
   path( "agency_edit/<int:agency_id>/",edit_agency,name="edit_agency"),
   path("agency_delete/<int:agency_id>/",delete_agency,name="delete_agency"),
   path("admin_setting",settings,name="admin_settings")

]
