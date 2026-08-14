from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns=[

        path('register/',register,name='regpage'),
        path('login/',login_view,name="login"),
        path("logout/",logout_view,name="logout"),
        path("register-agency/",register_agency,name="register_agency"),
        path("reports/",admin_reports,name="admin_reports"),
        path("settings/",admin_settings,name="admin_settings"),
        path("profile",profile_view,name="profile"),
        path("chatai",chatai,name="chatai"),
        path("travellers/",traveller_list,name="traveller_list"),
        path("add_traveller",add_traveller,name="add_traveller"),
        path("edit_traveller/<int:traveller_id>/",edit_traveller,name="edit_traveller"),
        path("delete_traveller/<int:traveller_id>/",delete_traveller,name="delete_traveller",),
        path("help/",help_center,name="help"),

]


urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

