#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append("../libs/")
import logging
import json
from common import log
import hashlib
import time
import urllib2
import redis
import os
class Redis_copy:
    rd = None
    def __init__(self, conf, log):
        self.conf_map = conf;
        self.log = log;
    def __open_redis(self):
        try:
            self.rd = redis.StrictRedis(host = self.conf_map['redisip'], port = int(self.conf_map['redisport']), db = int(self.conf_map['dbnumber']))
        except Exception, e:
            self.log.error(str(e))
            raise e;
            
    def save(self, dict):
        try:
            if self.rd == None :
                self.__open_redis()
            
        except Exception, e:
            raise e;
            
        
    def do_copy(self, dst_key,src_key, replace_item):
        ret = True
        try:
            if self.rd == None :
                self.__open_redis()
            self.log.debug(dst_key)   
        
          
            if self.rd.exists(src_key) != True:
                raise Exception("keys is not exists")
            
            self.log.debug(src_key)  
            data = self.rd.hgetall(src_key) 
            self.log.debug(str(data))
            if replace_item != None:
                for key in replace_item.keys():
                    data[key] = replace_item[key]
            
            for key in data.keys() :
                self.log.debug(dst_key+" "+key+" "+ data[key])
                
                self.rd.hset(dst_key, key, data[key])
            if dst_key[0] == "*" :
                self.rd.sadd('all-wildcard-domains', dst_key)
                self.log.debug("all-wildcard-domains add "+dst_key)
        except Exception, e:
            self.log.error(str(e))
            raise e
        
        return ret
            
#----------------------- main ------------------------------
if __name__ == '__main__' :


   
    logger = log.init_log(None)
    if logger == None :
        print " get logger fail"
        exit(-1)
    dst_key = sys.argv[1]
    src_key = sys.argv[2]

    conf_map ={
        "redisip":"127.0.0.1",
        "redisport":6379,
        "dbnumber":2,
        }
    logger.error(conf_map)
    rep ={
        "back_source_domain":dst_key,
        "domain_name":dst_key,
        
        }
    
    try:
        
        cp = Redis_copy(conf_map, logger)
        cp.do_copy(dst_key,src_key, rep)
    except Exception, e:
        logger.error(str(e))
    exit(-1)
