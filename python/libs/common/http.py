import logging
import logging.handlers
import httplib,urllib
import urlparse

class Http:
    log = None
    def __init__(self, log):
        self.log = log
    
    def Http_Post(self, url, data, headers):
        self.log.info("url %s",url);
        pu = urlparse.urlparse(url);
        self.log.debug(pu)

        self.log.debug("host:%s uri:%s args:%s", pu.netloc, pu.path, pu.query);       
        par = pu.netloc.split(":")
        host = par[0]
        port = 80
        if len(par) > 1:
            port = int(par[1])

        ctx ={ "host":host, "port": port, "uri": pu.path, "args": pu.query };
            
            
        self.log.debug(ctx);
        if headers != None :
            req_headers = headers
        else :
            req_headers = {}; 
        req_headers["Host"] = ctx['host'];
        http_client = None;
        resp_data = {"status": httplib.OK, "header" : {}, "data": None};
        self.log.debug(ctx);

        try:
            http_client = httplib.HTTPConnection(ctx['host'], ctx['port'], 10);    
            http_client.request("POST", ctx['uri'],data , req_headers);
            resp = http_client.getresponse();
            resp_data['status']= resp.status
            resp_data['header']= resp.getheaders();
            resp_data['data']= resp.read()
                 
        except Exception, e:
            self.log.error("http fail : url:[%s] [err:%s]", url,  str(e));
            resp_data['status']= 500;   
        
        if http_client != None :
            http_client.close();

        return resp_data; 


