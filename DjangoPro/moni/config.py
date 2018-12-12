#!/usr/bin/env python

# _*_ coding:utf-8 _*_
import configparser
import os
from ast import literal_eval


if not os.path.exists('moni.conf'):
    print('moni.conf is not exists')
    os._exit(1)

cf = configparser.ConfigParser()
try:
    cf.read('moni.conf')
except configparser.DuplicateOptionError as e:
    print('error:', e)

# moni config
moni_list = literal_eval(cf.get('moni', 'moni_ip'))    # 监控ip列表
patn_list = literal_eval(cf.get('moni', 'patn_list'))  #第三方IP,PORT列表
stan_list = literal_eval(cf.get('moni', 'stan_list'))  #警戒值列表
fw_list = literal_eval(cf.get('moni', 'fw_list'))  #服务器分组列表
