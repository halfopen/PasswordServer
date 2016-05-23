# -*- coding: utf-8 -*-
__author__ = 'halfopen'
from django.db import models


#
class WebSite(models.Model):
    url = models.CharField(max_length=256)
    username_html_id = models.CharField(max_length=256)
    password_html_id = models.CharField(max_length=256)

    def __unicode__(self):
        return "%s" % self.url


# 密码
class Password(models.Model):
    web_site = models.ForeignKey(WebSite)
    username = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    info = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return "%s @ %s" % (self.username, self.web_site)

