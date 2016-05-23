# -*- coding: utf-8 -*-
__author__ = 'halfopen'
import urllib2
import httplib
from django.http import HttpResponse
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist
from models import *
from api.FingerApi import FingerApi


def index(req):
    '''
    默认请求，用于指纹通过测试
    :param req:
    :return:
    '''
    api = FingerApi()
    result = api.confirm_user()
    return HttpResponse(result)


def get_password(req):
    """
    请求密码
    :param req:
    :return: 成功: ｛website:{url:,username_html_id:,password_html_id:,} , passwords:{[{username:,password:,info:,}],[]}｝
            失败: False
    """
    if "website" in req.GET:
        api = FingerApi()
        if api.confirm_user() is not True:  # 如果指纹认证没有通过
            return "False"
        website = req.GET['website']        # 获取要请求密码的网站
        try:
            return_val = {}                 # 定义返回变量

            website_object = WebSite.objects.get(url=website)
            website_info = {'url': website_object.url, 'username_html_id': website_object.username_html_id,
                            'password_html_id': website_object.password_html_id}  # 返回网站信息，用于自动填充
            return_val['website'] = website_info

            password_objects = Password.objects.filter(web_site=website_object)     # 获取该网站的所有密码
            passwords = []                  # 密码list
            password = {}                   # 单条密码
            for p in password_objects:
                password['username'] = p.username                                   # 返回密码
                password['password'] = p.password
                password['info'] = p.info
                passwords.append(password)

            return_val['passwords'] = passwords
            return render_json(return_val)  # 返回
        except ObjectDoesNotExist:
            return HttpResponse("False")    # 密码不存在
    return HttpResponse("False")            # 请求格式错误


def query_website(req):
    """
    返回网站信息
    :param req:
    :return:
    """
    if "website" in req.GET:
        website = req.GET['website']
        try:
            website_object = WebSite.objects.get(url=website)
            website_info = {'url': website_object.url, 'username_html_id': website_object.username_html_id,
                            'password_html_id': website_object.password_html_id}  # 返回网站信息，用于获取用户信息
            return render_json(website_info)
        except ObjectDoesNotExist:
            return HttpResponse("False")
    return HttpResponse("World")


def save_password(req):
    """
    保存密码
    :param req:
    :return:
    """
    if "website" in req.GET and 'username' in req.GET:
        if 'password' in req.GET:
            f = FingerApi()
            if f.confirm_user() is not True:            # 保存密码要求通过指纹验证
                return "False"
            url = req.GET['website']
            # print req.GET
            username = req.GET['username']
            password = req.GET['password']
            website = WebSite.objects.get(url=url)
            # print website
            password_obj = Password(web_site=website, username=username, password=password)
            password_obj.save()
            return HttpResponse("True")
    return HttpResponse("False")


def render_json(dic):
    '''
    返回 json 格式数据
    :param dic: 输入的变量
    :return: json
    '''
    json = simplejson.dumps(dic, ensure_ascii=False)
    mimetype = 'application/json'
    return HttpResponse(json, mimetype=mimetype)