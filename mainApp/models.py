from django.db import models

# Create your models here.


class User(models.Model):
    # 用户表
    user_gender = (
        (0, '男'),
        (1, '女'),
    )
    user_level = (
        (0, '最高权限'),
        (1, '管理权限'),
        (2, '基础权限'),
    )
    username = models.CharField(max_length=20, verbose_name='用户姓名')
    password = models.CharField(max_length=255, verbose_name='密码', null=False)
    gender = models.SmallIntegerField(choices=user_gender, default=0, verbose_name='性别')
    telephone = models.CharField(max_length=11, verbose_name='电话', null=True, blank=True)
    email = models.CharField(max_length=20, verbose_name='邮箱')
    level = models.SmallIntegerField(choices=user_level, default=2, verbose_name='用户权限')
    department = models.ForeignKey("Department", on_delete=models.CASCADE, verbose_name='部门')
    photo = models.CharField(max_length=30, verbose_name='用户头像', null=True, blank=True)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Department(models.Model):
    # 部门表
    dep_name = models.CharField(max_length=20, verbose_name='部门名称')
    dep_num = models.IntegerField(verbose_name='部门人数')
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.dep_name


class Order(models.Model):
    # 工单表
    ord_type_choice = (
        ('repair', '维修'),
        ('clean', '清洁'),
        ('security', '安保'),
    )
    ord_status = (
        (0, '未完成'),
        (1, '审核中'),
        (2, '已完成'),
    )
    ord_title = models.CharField(max_length=30, verbose_name='工单标题')
    ord_creator = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='创建者')
    telephone = models.CharField(max_length=20, verbose_name='联系电话', null=False)
    type = models.CharField(choices=ord_type_choice, max_length=30, verbose_name='报事类型', null=False)
    address = models.CharField(max_length=30, verbose_name='服务位置')
    receiver = models.CharField(max_length=20, verbose_name='接受人', null=True, blank=True)
    status = models.SmallIntegerField(choices=ord_status, default=0, verbose_name='工单状态')
    order_time = models.DateTimeField(verbose_name='预约时间')
    alter_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    ord_text = models.TextField()
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ord_title


class Announce(models.Model):
    # 公告表
    ann_title = models.CharField(max_length=20, verbose_name='公告标题')
    ann_creator = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='创建者')
    ann_text = models.TextField()
    effective_time = models.DateTimeField(verbose_name='有效时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    alter_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ann_title





