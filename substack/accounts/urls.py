
from django.urls import include, path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^$', views.send_to_login, name='homepage'),
    re_path(r'^login/$', views.login_screen, name='login'),
    re_path(r'^signup/$', views.create_account, name='create'),
    re_path(r'^create/$', views.create_account, name='signup'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^profile/$', views.account_profile, name='profile')
]

htmxpatterns = [
    re_path(r'^details/$', views.show_account, name='account-home'),
    re_path(r'^details/saved/$', views.detail_snippet, name="detail-snippet"),
    re_path(r'^details/edit/$', views.edit_snippet, name='edit-snippet'),
    re_path(r'^signup/verify-email/', views.verify_email, name="verify-email")
]

urlpatterns += htmxpatterns