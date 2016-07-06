#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import os
import urlparse
import hashlib
import argparse

def get_md5_value(src):
    Md5 = hashlib.md5()
    Md5.update(src)
    Md5_Digest = Md5.hexdigest()
    return Md5_Digest

def create_s3(ctx):
    pu = urlparse.urlparse(ctx['url']);
    print pu
    uri = pu.path
    e = long(time.time())+ int(ctx['timeout'])
    
    sign =get_md5_value(uri+ str(e)+ctx['secret'])
    ret = "%s?e=%s&sign=%s" %(str(ctx['url']),str(e),str(sign))
    return [ret,sign, pu.netloc]

def parse_args():
    parser = argparse.ArgumentParser(description='auto create s3 secret url')
    parser.add_argument('url', action='store',  help='Storea simple value')
    parser.add_argument('-t', action='store',dest='timeout' ,type= int, help='Storea simple value')
    parser.add_argument('-s', action='store', dest='secret', help='Storea simple value')              
    args = parser.parse_args()
    
       
    print args
    return args
    
def get_ctx(args):
    print args
    ctx ={
        "url": args.url,
        "timeout": args.timeout or 30,
        "secret" : args.secret or "d86d73cec3d3b2c790ad8f53644946ba"
    }
    
    return ctx;

#----------------------- main ------------------------------
if __name__ == '__main__' :
   
    args = parse_args()
  
    ctx = get_ctx(args)
    if ctx == None :
        exit(-1)

    print ctx
    try:
        
        list =create_s3(ctx)
        curl_opt = [
                 "curl -v -o/dev/null -x 127.0.0.1:80",
                 " \"%s\"" %(list[0]), 
                 " -H \"Authorization: %s\"" % (list[1]),
                 " -H \"Refer: http://%s\"" %(list[2])
                ]
        cmd =""
        for i in range(0,len(curl_opt)):
            cmd += curl_opt[i]
        print cmd
    
        os.system(cmd) 
    except Exception, e:
        print str(e)

    exit(-1)
