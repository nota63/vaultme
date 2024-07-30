from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
import pywhatkit as kit
import psutil
import datetime


# main
def main(request):
    return render(request, 'main.html')


@login_required
def developer_platform(request):
    messages.success(request, 'successfully reached to developers room')
    return render(request, 'developer_platform.html')


@login_required
def about(request):
    return render(request, 'about.html')


@login_required
def shutdown(request):
    kit.shutdown(time=1)
    return render(request, 'shutdown.html')


@login_required
def system_info_view(request):
    system_info = {
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'cpu_count_physical': psutil.cpu_count(logical=False),
        'cpu_times': psutil.cpu_times(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'virtual_memory': psutil.virtual_memory(),
        'swap_memory': psutil.swap_memory(),
        'disk_partitions': psutil.disk_partitions(),
        'disk_usage': psutil.disk_usage('/'),
        'disk_io': psutil.disk_io_counters(),
        'net_if_addrs': psutil.net_if_addrs(),
        'net_io': psutil.net_io_counters(),
        'battery': psutil.sensors_battery(),
        'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()),
    }
    return render(request, 'system_info.html', {'system_info': system_info})


# task manager view
@login_required
def task_manager(request):
    return render(request, 'task_manager.html')

