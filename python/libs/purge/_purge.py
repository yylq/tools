import logging
import logging.handlers
import httplib,urllib
import urlparse

def get_http_client(server_ip, port, time_out, log) : 
    httpClient = None;
    try:
        httpClient  = httplib.HTTPConnection(server_ip, port, timeout = time_out);
    except Exception, e:
        log.error("%s",str(e));
        return None;
    return httpClient;

def get_purge_ctx(url, proxy, log, flag):
    log.info("url %s",url);
    pu = urlparse.urlparse(url);
    par= proxy.split(':')
    proxy_host = par[0]
    proxy_port = 80
    if len(par) >= 2 :
        proxy_port = int(par[1])

    log.info("host:%s uri:%s args:%s", pu.netloc, pu.path, pu.query);       
    ctx ={"status" : httplib.OK,
        "url" : url, "proxy_host" :proxy_host, "proxy_port":proxy_port,
        "host" : pu.netloc, "uri" :pu.path, "args" : pu.query,
        "fsize": 0, "slice_size" : 0 ,"ind" : 0, "finish" : False};
        
    log.info(ctx);

    headers = {"Host" : ctx['host']};
    if flag =="store" :
        headers["Purge-info"] = "true"
    http_client = None;
    try:
        http_client = get_http_client(ctx['proxy_host'], ctx['proxy_port'], 10, log);    
        http_client.request("HEAD", ctx['uri'], None, headers);
        resp = http_client.getresponse();
        resp.read();
        log.info(resp.getheaders());
        ctx['status'] = resp.status
        if resp.status == httplib.OK :
            ctx['slice_size'] = int(resp.getheader('slice-size')) + 1;
            ctx['fsize'] = int(resp.getheader('Content-Length'));
        
             
    except Exception, e:
        log.error("purge ctx fail : url:[%s] [err:%s]", url,  str(e));
        ctx['status'] = httplib.INTERNAL_SERVER_ERROR
    
    if http_client != None :
        http_client.close();

    return ctx; 

def purge_url(url, proxy_host, log, flag):
    ctx = get_purge_ctx(url, proxy_host, log, flag);    
    if ctx['status'] != httplib.OK :
        if flag == "store" and ctx['status'] > 500 :
            return httplib.OK 

        log.error("purge ctx fail : url:[%s]", url);
        return ctx['status'];
        
    headers = {"Host" : ctx['host']};
    http_client = None;
    http_client = get_http_client(ctx['proxy_host'], ctx['proxy_port'], 10, log);    
    while not ctx['finish'] :
        if ctx['ind'] * ctx['slice_size'] > ctx['fsize'] :
            ctx['finish'] = True;
            continue;
        headers['Range'] = "bytes=" + str(ctx['ind'] * ctx['slice_size'])+ "-";
        log.debug(headers);
        try:
        #   http_client = get_http_client(ctx['proxy_host'], 80,10);    
            http_client.request("PURGE", ctx['uri'], None, headers);
            resp = http_client.getresponse();
            resp.read();
            if resp.status == httplib.OK or  resp.status == httplib.NOT_FOUND :
                log.info("purge sucess:[%s][%s] [status:%d]", url, headers['Range'], resp.status );
            else :
                log.error("purge fail:[%s][%s] [status:%d]", url, headers['Range'], resp.status );
    
        except Exception, e:
            log.error("purge fail:[%s][%s] [err:%s]", url, headers['Range'], str(e));
            ctx['status'] = httplib.INTERNAL_SERVER_ERROR
            break;      
        ctx['ind'] +=1;

    if http_client == None :
        http_client.close();
    
    log.debug(ctx);
    
    return ctx['status'] 


