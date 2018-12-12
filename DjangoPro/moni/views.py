from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Avg
from .models import *
from .config import *
import datetime, json, sys, math


# Create your views here.
def Login(request):
    context = {'error_name': 0, 'error_pwd': 0}
    return render(request, 'moni/login.html',context)


def Login_handle(request):
    uname = request.POST.get('username')
    upwd = request.POST.get('pwd')
    users = UserInfo.objects.filter(uname=uname)
    if len(users) == 1:
        if users[0].upwd == upwd:
            request.session['user_id'] = users[0].id
            # request.session.set_expiry(0)
            return redirect(reverse('Index'))
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'moni/login.html', context)
    else:
        context = {'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'moni/login.html', context)


def Logout(request):
    request.session.flush()
    return redirect('Login')


def Is_login(func):
    def loginfuc(request, *args, **kwargs):
        print(request.session.get('user_id'))
        if request.session.get('user_id'):
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/moni/login')
            return red

    return loginfuc


@Is_login
def Index(request):
    return render(request, 'moni/index.html')


def GetMchInfo(ip):
    sta_list = []
    patn_stat = []
    # dt = (datetime.datetime.now()-datetime.timedelta(days=8)-datetime.timedelta(seconds=60))
    dt = datetime.datetime(2018, 10, 17, 0, 0, 0)

    netinfo = NetInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if netinfo == None:
        sta_list.append('1')
    else:
        sta_list.append('0')

    platinfo = PlatInfo.objects.filter(ip=ip).order_by('time').first()
    if platinfo == None:
        sta_list.append('1')
    else:
        sta_list.append('0')

    if len(patn_list) != 0:
        for p in patn_list:
            patn = p.split(':')
            patninfo = PartnerInfo.objects.filter(time__gte=dt, ip=ip, p_ip=patn[0], p_port=patn[1]).order_by('time').first()
            if patninfo == None:
                patn_stat.append('1')
            else:
                patn_stat.append('0')
        if '1' in patn_stat:
            sta_list.append('1')
        else:
            sta_list.append('0')
    else:
        sta_list.append('0')

    cpuinfo = CpuInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if cpuinfo == None:
        sta_list.append('1')
    else:
        pct = (float)(cpuinfo.percent)
        round(pct, 2)
        if pct - stan_list[0] <= 0:
            sta_list.append('0')
        else:
            sta_list.append('1')

    meminfo = MemInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if meminfo == None:
        sta_list.append('1')
    else:
        pct = (float)(meminfo.percent)
        round(pct, 2)
        if pct - stan_list[1] <= 0:
            sta_list.append('0')
        else:
            sta_list.append('1')

    swapinfo = SwapInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if swapinfo == None:
        sta_list.append('1')
    else:
        pct = (float)(swapinfo.percent)
        round(pct, 2)
        if pct - stan_list[2] <= 0:
            sta_list.append('0')
        else:
            sta_list.append('1')

    diskinfo = DiskInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if diskinfo == None:
        sta_list.append('1')
    else:
        pct = (float)(diskinfo.percent)
        round(pct, 2)
        if pct - stan_list[3] <= 0:
            sta_list.append('0')
        else:
            sta_list.append('1')
    # print(ip,sta_list)
    return sta_list


@Is_login
def MoniMchInfo(request):
    data = []
    for ip in moni_list:
        if '1' in GetMchInfo(ip):
            data.append([ip.split('.')[3],'1'])
        else:
            data.append([ip.split('.')[3], '0'])
    # print(data)
    return render(request, 'moni/monimchinfo.html',{'data':data,'fwlist':fw_list})

def MoniMchInfoHandle(request):
    data = []
    for ip in moni_list:
        if '1' in GetMchInfo(ip):
            data.append([ip.split('.')[3],'1'])
        else:
            data.append([ip.split('.')[3], '0'])
    return JsonResponse({'data_list':data})

def CoutDate():
    today = datetime.date.today()
    daylist = []
    for i in range(7):
        day = today - datetime.timedelta(days=7 - i)
        daylist.append(day.strftime('%Y-%m-%d'))
    return daylist


def GetAvgNetInfo(ip, date_list):
    '''ip 为网络地址 date为日期'''
    data_list = []
    netin_list = []
    netout_list = []
    mem_list = []
    cpu_list = []
    swap_list = []
    disk_list = []

    for dt in date_list:
        netinfo = NetInfo.objects.filter(ip=ip, time__startswith=dt).aggregate(recv=Avg('recv'), sent=Avg('sent'))
        if netinfo['recv'] == None:
            netin = 0.00
        else:
            netin = netinfo['recv'] / 1024

        if netinfo['sent'] == None:
            netout = 0.00
        else:
            netout = netinfo['sent'] / 1024
        netin = round(netin, 2)
        netin_list.append(netin)
        netout = round(netout, 2)
        netout_list.append(netout)

        meminfo = MemInfo.objects.filter(ip=ip, time__startswith=dt).aggregate(pct=Avg('percent'))
        if meminfo['pct'] == None:
            mem_list.append(0.00)
        else:
            mem_list.append(round(meminfo['pct'], 2))

        cpuinfo = CpuInfo.objects.filter(ip=ip, time__startswith=dt).aggregate(pct=Avg('percent'))
        if cpuinfo['pct'] == None:
            cpu_list.append(0.00)
        else:
            cpu_list.append(round(cpuinfo['pct'], 2))

        swapinfo = SwapInfo.objects.filter(ip=ip, time__startswith=dt).aggregate(pct=Avg('percent'))
        if swapinfo['pct'] == None:
            swap_list.append(0.00)
        else:
            swap_list.append(round(swapinfo['pct'], 2))

        diskinfo = DiskInfo.objects.filter(ip=ip, time__startswith=dt).aggregate(pct=Avg('percent'))
        if diskinfo['pct'] == None:
            disk_list.append(0.00)
        else:
            disk_list.append(round(diskinfo['pct'], 2))

    mem_list = list((1, mem_list))
    cpu_list = list((2, cpu_list))
    swap_list = list((3, swap_list))
    disk_list = list((4, disk_list))
    netin_list = list((5, netin_list))
    netout_list = list((6, netout_list))

    return (list((mem_list, cpu_list, swap_list, disk_list, netin_list, netout_list)))


@Is_login
def MoniAvgPage(request):
    # date_list = CoutDate()
    date_list = ['2018-10-11', '2018-10-12', '2018-10-13', '2018-10-14', '2018-10-15', '2018-10-16', '2018-10-17']
    page = request.GET.get('page', 1)
    curPage = int(page)
    if curPage == 1:
        prePage = None
    else:
        prePage = curPage - 1

    if curPage == len(moni_list):
        nexPage = None
    else:
        nexPage = curPage + 1

    startPage = 1
    endPage = len(moni_list)

    data_list = list((moni_list[curPage - 1], date_list))
    data_list.append(GetAvgNetInfo(moni_list[curPage - 1], date_list))

    return render(request, 'moni/moniavgpage.html',
                  {'list': data_list,
                   'startPage': startPage,
                   'curPage': curPage,
                   'prePage': prePage,
                   'nexPage': nexPage,
                   'endPage': endPage,
                   })


@Is_login
def MoniAvgPageOne(request):
    # date_list = CoutDate()
    date_list = ['2018-10-11', '2018-10-12', '2018-10-13', '2018-10-14', '2018-10-15', '2018-10-16', '2018-10-17']
    ip = request.GET.get('IP')

    if ip == None:
        return HttpResponse('ip is None')
    else:
        data_list = [ip, date_list]
        data_list.append(GetAvgNetInfo(ip, date_list))
    print(data_list)
    return render(request, 'moni/moniavgpageone.html', {'list': data_list})


def GetCurMoniInfo(ip):
    pct_list = []
    ext_list = []
    patn_sta = []
    # today = datetime.date.today().strftime('%Y-%m-%d')
    # dt = (datetime.datetime.now()-datetime.timedelta(days=8)-datetime.timedelta(seconds=60))
    dt = datetime.datetime(2018, 10, 17, 0, 0, 0)

    netinfo = NetInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if netinfo == None:
        net_sta = 1
        net_in = '0.00'
        net_out = '0.00'
    else:
        net_sta = 0
        net_in = '%.2f' % (netinfo.recv / 1024)
        net_out = '%.2f' % (netinfo.sent / 1024)

    platinfo = PlatInfo.objects.filter(ip=ip).order_by('time').first()
    if platinfo == None:
        pmch = '未知'
        psys = '未知'
    else:
        pmch = platinfo.machine
        psys = platinfo.system

    for p in patn_list:
        patn = p.split(':')
        patninfo = PartnerInfo.objects.filter(time__gte=dt, ip=ip, p_ip=patn[0], p_port=patn[1]).order_by(
            'time').first()
        if patninfo == None:
            ping_sta = 'False'
            port_sta = 'False'
        else:
            ping_sta = patninfo.ping
            port_sta = patninfo.port_status
        patn_sta.append(list((patn[0], patn[1], ping_sta, port_sta)))

    cpuinfo = CpuInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if cpuinfo == None:
        cpct = json.dumps('')
        ext_list.append(json.dumps(''))
    else:
        pct = (float)(cpuinfo.percent)
        round(pct, 2)
        if pct - stan_list[0] <= 0:
            if pct <= 0:
                cpct = json.dumps('')
            else:
                cpct = pct
            ext_list.append(json.dumps(''))
        else:
            cpct = stan_list[0]
            ext_list.append(round(pct - stan_list[0], 2))
    pct_list.append(cpct)

    meminfo = MemInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if meminfo == None:
        mpct = json.dumps('')
        ext_list.append(json.dumps(''))
    else:
        pct = (float)(meminfo.percent)
        round(pct, 2)
        if pct - stan_list[1] <= 0:
            if pct <= 0:
                mpct = json.dumps('')
            else:
                mpct = pct
            ext_list.append(json.dumps(''))
        else:
            mpct = stan_list[1]
            ext_list.append(round(pct - stan_list[1], 2))
    pct_list.append(mpct)

    swapinfo = SwapInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if swapinfo == None:
        spct = json.dumps('')
        ext_list.append(json.dumps(''))
    else:
        pct = (float)(swapinfo.percent)
        round(pct, 2)
        if pct - stan_list[2] <= 0:
            if pct <= 0:
                spct = json.dumps('')
            else:
                spct = pct
            ext_list.append(json.dumps(''))
        else:
            spct = stan_list[2]
            ext_list.append(round(pct - stan_list[2], 2))
    pct_list.append(spct)

    diskinfo = DiskInfo.objects.filter(time__gte=dt, ip=ip).order_by('time').first()
    if diskinfo == None:
        dpct = json.dumps('')
        ext_list.append(json.dumps(''))
    else:
        pct = (float)(diskinfo.percent)
        round(pct, 2)
        if pct - stan_list[3] <= 0:
            if pct <= 0:
                dpct = json.dumps('')
            else:
                dpct = (int)(diskinfo.percent)
            ext_list.append(json.dumps(''))
        else:
            dpct = stan_list[3]
            ext_list.append(round(pct - stan_list[3], 2))
    pct_list.append(dpct)

    return (list((ip, pmch, psys, net_sta, patn_sta, net_in, net_out, pct_list, ext_list)))


@Is_login
def MoniCurPage(request):
    ip_list = []
    ip_io = []
    context = []
    netinfo = moni_list
    num = len(netinfo)
    if num == 0:
        return HttpResponse('not moni cfg')
    else:
        for i in netinfo:
            ip_io.append(GetCurMoniInfo(i))
    paginator = Paginator(ip_io, 4)
    page = request.GET.get('page', 1)
    currentPage = int(page)
    try:
        context = paginator.page(currentPage)  # 获取当前页码的记录
    except PageNotAnInteger:
        context = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        context = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'moni/monipage.html', {'io': context, 'paginator': paginator, 'currentPage': currentPage})


@Is_login
def MoniCurPageOne(request):
    ip = request.GET.get('IP')
    if ip == None:
        return HttpResponse('ip is None')
    else:
        context = GetCurMoniInfo(ip)
        return render(request, 'moni/monipageone.html', {'io': context})
