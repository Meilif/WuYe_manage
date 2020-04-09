from django import forms
from django.forms import widgets
from mainApp.models import Order, Announce, User


# 用户登录表单
class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128)
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput)


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'ord_title',
            'ord_creator',
            'telephone',
            'type',
            'address',
            'order_time',
            'ord_text'
        )
        labels = {
            'ord_title': '标题',
            'ord_creator': '创建者',
            'telephone': '联系电话',
            'type': '报事类型',
            'address': '服务地址',
            'order_time': '预定时间',
            'ord_text': '正文'
        }
        widgets = {
            'order_time': widgets.DateTimeInput(attrs={'type': 'date'}),

        }


class AnnounceModelForm(forms.ModelForm):
    class Meta:
        model = Announce
        fields = (
            'ann_title',
            'ann_creator',
            'ann_text',
            'effective_time'
        )
        labels = {
            'ann_title': '标题',
            'ann_creator': '创建者',
            'ann_text': '正文',
            'effective_time': '有效时间'
        }
        widgets = {
            'effective_time': widgets.DateTimeInput(attrs={'type': 'date'})
        }


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'gender',
            'telephone',
            'email',
            'level',
            'department'
        )
        labels = {
            'username': '姓名',
            'password': '密码',
            'gender': '性别',
            'telephone': '电话',
            'email': '电子邮件',
            'level': '权限级别',
            'department': '部门'
        }
        widgets = {}



