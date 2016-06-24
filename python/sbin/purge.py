#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import stat
import os
import logging
import logging.handlers
import httplib,urllib
import urlparse
import _purge

VERSION_INFO        = "0.0.0.1";
MAX_LOG_FILE_SIZE   = 64 * 1024 * 1024;
MAX_LOG_FILE_ROTATE = 10;

g_logger = None;

def init_log():
    global g_logger;
    g_logger = logging.getLogger();
    formatter = logging.Formatter('%(asctime)s|%(funcName)s|%(lineno)d|%(thread)d|%(levelname)s|%(message)s');
    hdlr = logging.handlers.RotatingFileHandler('./purge.log', 'a', MAX_LOG_FILE_SIZE, MAX_LOG_FILE_ROTATE);
    hdlr.setFormatter(formatter);
    g_logger.addHandler(hdlr);

    stream_hdlr = logging.StreamHandler(sys.stdout);
    stream_hdlr.setFormatter(formatter);
    g_logger.addHandler(stream_hdlr);

    g_logger.setLevel(logging.NOTSET);

    g_logger.info("%s - Version: %s",sys.argv[0], VERSION_INFO);    

def useage():
    print "useage:%s url [flag=cache|store]" % sys.argv[0];


#----------------------- main ------------------------------
if __name__ == '__main__' :
    argc = len(sys.argv);
    print "%d" % argc;
    if argc  < 2 :
        useage();
        exit(-1);
    
    url = sys.argv[1];
    flag = "cache"
    proxy_host = "127.0.0.1:80"
    if argc >=2 :
        flag = sys.argv[2] 
    if flag == "store" :
	proxy_host = "127.0.0.1:8080" 
    init_log(); 
    
    g_logger.info("purge host:%s url:%s", proxy_host, url);     
    st=_purge.purge_url(url, proxy_host, g_logger, flag);
    g_logger.info(st)
    exit(-1)
    #sys.exit(-1)
