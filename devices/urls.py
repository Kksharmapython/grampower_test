from django.urls import path

from devices.views import auth_login, login_page, device_detail, logout_a

urlpatterns = [
    path("loginUser/", auth_login, name="auth_login"),
    path("logout_a/", logout_a, name="logout_a"),
        path("device/<str:meter_address>/", device_detail, name="device_detail"),
    path("", login_page, name="login_page")
]
