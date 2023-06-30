from django import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.db.models import Avg
from .models import Devices, get_all_device_date

from django.db.models import ExpressionWrapper, DecimalField , F, Sum

def total_consumptions(devices):
    import datetime
    first_day_date = datetime.datetime.strptime(devices.first().meter_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
    second_date= datetime.datetime.strptime(devices.last().meter_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S') 
    days= second_date - first_day_date
    total_power = devices.aggregate(sub_total=Sum(F("apparent_power_VA")))["sub_total"]

    return total_power*((days.seconds/60)/1000)
    


def login_page(request):
    if request.session.get("username"): 
        devices = Devices.objects.all()
        context = {"devices": Devices.objects.all(), "length_of_device": len(devices)}
        return render(request, "device_list.html", context)
    return render(request, "login.html", )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auth_login(request):
    try:
        user = None
        if request.session.get("username"):
            user = User.objects.get(
                username=request.session.get("username")
            )
        if request.POST.get("username"):
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            request.session["username"] = user.username
            devices = Devices.objects.all()
            context = {"devices": Devices.objects.all(), "length_of_device": len(devices)}
            return render(request, "device_list.html", context)
        return render(request, "login.html", )
    except User.DoesNotExist:
        return render(request, "login.html", )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def device_detail(request, meter_address):
    if request.session.get("username"):
        try:
            device_query_set = Devices.objects.filter(meter_address=meter_address)
            avg = device_query_set.aggregate(avg_voltage=ExpressionWrapper(Avg(F("voltage")), DecimalField()), avg_current=ExpressionWrapper(Avg(F("apparent_power_VA")), DecimalField()))
            get_all_device_date()
            return render(request, "device_detail.html",
                          {"device":Devices.objects.get(public_id=device_query_set[0].public_id),"avg_current":avg["avg_current"] ,"avg_voltage": avg.get("avg_voltage"), "total_consmp":total_consumptions(device_query_set), "last_data_point":device_query_set.last().meter_time})
        except Devices.DoesNotExist:
            devices = Devices.objects.all()

            context = {"devices": Devices.objects.all(), "length_of_device": len(devices)}
            return render(request, "device_list.html", context)
    return render(request, "login.html", )


def logout_a(request):
    if request.session.get("username"):
        del request.session["username"]
        print(request.session.get("username"))
        request.session["username"] = None
        request.session.modified = True
        request.session.flush()
    return render(request, "login.html", )
