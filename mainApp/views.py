from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Q
from mainApp import models
from . import form

# Create your views here


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    ann = models.Announce.objects.all().order_by("create_time").exclude(isDelete=True)
    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
    return render(request, 'index.html', {'ann': ann, 'orders': orders})


def base(request):
    return render(request, 'base.html')


def cre_ann(request):
    announce_form = form.AnnounceModelForm()
    if request.method == 'POST':
        announce_form = form.AnnounceModelForm(request.POST)
        message = '请检查填写的内容！'
        if announce_form.is_valid():
            ann_title = announce_form.cleaned_data.get('ann_title')
            ann_creator = announce_form.cleaned_data.get('ann_creator')
            eff_time = announce_form.cleaned_data.get('effective_time')
            ann_text = announce_form.cleaned_data.get('ann_text')

            new_ann = models.Announce()
            new_ann.ann_title = ann_title
            new_ann.ann_creator = ann_creator
            new_ann.effective_time = eff_time
            new_ann.ann_text = ann_text
            new_ann.save()
            message = '创建成功! '
        else:
            message = '提交失败'
            return render(request, 'create_announce.html', locals())

        announce_form = form.AnnounceModelForm()
        return render(request, 'create_announce.html', locals())
    return render(request, 'create_announce.html', locals())


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        login_form = form.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                users = models.User.objects.get(Q(username=username) | Q(email=username))
            except:
                message = '用户不存在！'
                return render(request, 'login.html', locals())

            if users.password == password:
                dep = models.Department.objects.get(dep_name=users.department)
                request.session['is_login'] = True
                request.session['user_id'] = users.id
                request.session['user_name'] = users.username
                request.session['user_gender'] = users.gender
                request.session['user_department'] = dep.dep_name
                request.session['user_email'] = users.email
                request.session['user_level'] = users.level
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = form.UserForm()
    return render(request, 'login.html')


def order(request, status):
    if status == 0:
        orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})
    elif status == 1:
        orders = models.Order.objects.filter(Q(receiver=request.session['user_name'])
                                             | Q(ord_creator=request.session['user_id']))\
            .exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})
    elif status == 2:
        orders = models.Order.objects.filter(status=0).exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})
    elif status == 3:
        orders = models.Order.objects.filter(status=1).exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})
    else:
        orders = models.Order.objects.filter(status=2).exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})


def cre_ord(request):
    order_form = form.OrderModelForm()
    if request.method == 'POST':
        order_form = form.OrderModelForm(request.POST)
        message = '请检查填写的内容！'
        if order_form.is_valid():
            order_title = order_form.cleaned_data.get('ord_title')
            order_creator = order_form.cleaned_data.get('ord_creator')
            telephone = order_form.cleaned_data.get('telephone')
            ord_type = order_form.cleaned_data.get('type')
            address = order_form.cleaned_data.get('address')
            ord_time = order_form.cleaned_data.get('order_time')
            ord_text = order_form.cleaned_data.get('ord_text')

            new_order = models.Order()
            new_order.ord_title = order_title
            new_order.telephone = telephone
            new_order.ord_creator = order_creator
            new_order.type = ord_type
            new_order.address = address
            new_order.order_time = ord_time
            new_order.ord_text = ord_text
            new_order.save()
            message = '创建成功! '
        else:
            message = '提交失败'
            return render(request, 'create_order.html', locals())

        order_form = form.OrderModelForm()
        return render(request, 'create_order.html', locals())
    return render(request, 'create_order.html', locals())


def user(request):
    users = models.User.objects.all().exclude(isDelete=True)
    return render(request, 'user.html', {'users': users})


def announce(request):
    ann = models.Announce.objects.all().order_by("create_time").exclude(isDelete=True)
    return render(request, 'announce.html', {'ann': ann})


def alter_user(request, uid):
    users = models.User.objects.filter(pk=uid)
    if request.method == 'POST':
        # 读取输入的数据
        name = request.POST.get('name')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        if gender == '男':
            gender = 0
        elif gender == '女':
            gender = 1
        # 修改数据库
        users = models.User.objects.get(pk=uid)
        users.username = name
        if password:
            users.password = password
        users.email = email
        users.gender = gender
        users.save()
        # 修改session
        if uid == request.session['user_id']:
            request.session.clear()
            return redirect('/login/')
        else:
            request.session['message'] = '修改成功'
            users = models.User.objects.all()
            return render(request, 'user.html', {'users': users})
    return render(request, 'alter_user.html', {"users": users})


def alter_ord(request, uid):
    orders = models.Order.objects.filter(pk=uid)
    if request.method == 'POST':
        # 读取输入的数据
        title = request.POST.get('title')
        telephone = request.POST.get('telephone')
        types = request.POST.get('type')
        if types == '维修':
            types = 'repair'
        elif types == '清洁':
            types = 'clean'
        else:
            types = 'security'
        address = request.POST.get('address')
        order_time = request.POST.get('order_time')
        text = request.POST.get('ord_text')
        # 修改数据库
        orders = models.Order.objects.get(pk=uid)
        orders.ord_title = title
        orders.telephone = telephone
        orders.type = types
        orders.address = address
        if order_time:
            orders.order_time = order_time
        orders.ord_text = text
        orders.save()
        request.session['message'] = '修改成功'
        orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
        return render(request, 'order.html', {'orders': orders})
    return render(request, 'alter_ord.html', {'orders': orders})


def alter_ann(request, uid):
    ann = models.Announce.objects.filter(pk=uid)
    if request.method == 'POST':
        # 读取输入的数据
        title = request.POST.get('title')
        effective_time = request.POST.get('order_time')
        text = request.POST.get('ord_text')
        # 修改数据库
        ann = models.Announce.objects.get(pk=uid)
        ann.ann_title = title
        if effective_time:
            ann.order_time = effective_time
        ann.ann_text = text
        ann.save()
        request.session['message'] = '修改成功'
        ann = models.Announce.objects.all().order_by("create_time").exclude(isDelete=True)
        return render(request, 'announce.html', {'ann': ann})
    return render(request, 'alter_ann.html', {'ann': ann})


def catch_order(request, uid):
    orders = models.Order.objects.filter(pk=uid)
    for orders in orders:
        if orders.receiver:
            message = '工单已被接取'
            orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
            return render(request, 'order.html', locals())
        else:
            if orders.type == 'repair':
                if request.session['user_department'] == '工程部':
                    message = '成功接取维修工单'
                    orders.receiver = request.session['user_name']
                    orders.save()
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
                else:
                    message = '对不起，您的部门无法接取此类工单'
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
            elif orders.type == 'clean':
                if request.session['user_department'] == '环卫部':
                    message = '成功接取清洁工单'
                    orders.receiver = request.session['user_name']
                    orders.save()
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
                elif request.session['user_department'] == '环境部':
                    message = '成功接取清洁工单'
                    orders.receiver = request.session['user_name']
                    orders.save()
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
                else:
                    message = '对不起，您的部门无法接取此类工单'
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
            else:
                if request.session['user_department'] == '秩序部':
                    message = '成功接取安保工单'
                    orders.receiver = request.session['user_name']
                    orders.save()
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
                if request.session['user_department'] == '消控室':
                    message = '成功接取安保工单'
                    orders.receiver = request.session['user_name']
                    orders.save()
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())
                else:
                    message = '对不起，您的部门无法接取此类工单'
                    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
                    return render(request, 'order.html', locals())


def pass_order(request, uid, status):
    orders = models.Order.objects.filter(pk=uid)
    if status == 0:
        return render(request, 'pass_ord.html', {'orders': orders})
    elif status == 1:
        for orders in orders:
            orders.status = 2
            orders.save()
            message = '审核通过'
            orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
            return render(request, 'order.html', locals())
    elif status == 2:
        for orders in orders:
            orders.status = 0
            orders.save()
            message = '审核未通过'
            orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
            return render(request, 'order.html', locals())


def refer_order(request, uid):
    orders = models.Order.objects.filter(pk=uid)
    for orders in orders:
        orders.status = 1
        orders.save()
        message = '工单提交审核'
        orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
        return render(request, 'order.html', locals())


def cre_user(request):
    user_form = form.UserModelForm()
    if request.method == 'POST':
        user_form = form.UserModelForm(request.POST)
        message = '请检查填写的内容！'
        if user_form.is_valid():
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password')
            gender = user_form.cleaned_data.get('gender')
            telephone = user_form.cleaned_data.get('telephone')
            email = user_form.cleaned_data.get('email')
            level = user_form.cleaned_data.get('level')
            department = user_form.cleaned_data.get('department')
            departments = models.Department.objects.get(dep_name=department)

            new_user = models.User()
            new_user.username = username
            new_user.password = password
            new_user.gender = gender
            new_user.telephone = telephone
            new_user.email = email
            new_user.level = level
            new_user.department = department
            departments.dep_num = departments.dep_num + 1
            departments.save()
            new_user.save()
            message = '创建成功! '
        else:
            message = '提交失败'
            return render(request, 'create_user.html', locals())
        user_form = form.UserModelForm()
        return render(request, 'create_user.html', locals())
    return render(request, 'create_user.html', locals())


def page_not_found(request):
    return render(request, '404.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def del_ann(request, uid):
    ann = models.Announce.objects.get(pk=uid)
    ann.isDelete = True
    ann.save()
    ann = models.Announce.objects.all().order_by("create_time").exclude(isDelete=True)
    return render(request, 'announce.html', {'ann': ann})


def del_ord(request, uid):
    orders = models.Order.objects.get(pk=uid)
    orders.isDelete = True
    orders.save()
    orders = models.Order.objects.all().order_by("create_time").exclude(isDelete=True)
    return render(request, 'order.html', {'orders': orders})


def del_user(request, uid):
    users = models.User.objects.get(pk=uid)
    users.isDelete = True
    users.save()
    users = models.User.objects.all().exclude(isDelete=True)
    return render(request, 'user.html', {'users': users})