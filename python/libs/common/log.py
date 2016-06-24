import sys
import logging
import logging.handlers
import types
MAX_LOG_FILE_SIZE   = 64 * 1024 * 1024;
MAX_LOG_FILE_ROTATE = 10;
DEFUALT_LOG_FORMATTER = '%(asctime)s|%(filename)s|%(lineno)d|%(levelname)s|%(message)s'
    
def init_log_ctx(conf):
    ctx = {
        "max_log_size": MAX_LOG_FILE_SIZE,
        "max_log_rotate": MAX_LOG_FILE_ROTATE,
        "log_formatter": DEFUALT_LOG_FORMATTER,
        "log_level": logging.DEBUG,
        "log_file": "",
        "to_console": 1 }
    if conf == None :
        return ctx
    try:
        if 'max_log_size' in conf.keys() :
            ctx['max_log_size'] = int(conf['max_log_size'])
        if 'max_log_rotate' in conf.keys():
            ctx['max_log_rotate'] = int(conf['max_log_rotate'])
        if 'log_formatter' in conf.keys():
            ctx['log_formatter'] = conf['log_formatter']
        if 'log_level' in conf.keys() :
            ctx['log_level'] = int(conf['log_level'])   
        if 'log_file' in conf.keys() :
            ctx['log_file'] = conf['log_file']

        if ctx['log_file'] != "" and 'to_console' in conf.keys() :
            ctx['to_console'] = int(conf['to_console'])
        
    except Exception, e:
        print "init ctx fail %s" % str(e)
    return ctx;

def init_log(conf) :
    logger = None
     
    try:
        ctx = init_log_ctx(conf)
        logger = logging.getLogger();
        logger.setLevel(ctx['log_level']);
        hd_fm = logging.Formatter(ctx['log_formatter']); 
        if ctx['log_file'] != "" :
            hdlr = logging.handlers.RotatingFileHandler(ctx['log_file'], 'a', ctx['max_log_size'], ctx['max_log_rotate']);
            hdlr.setFormatter(hd_fm);
            logger.addHandler(hdlr);
        
        if ctx['to_console'] == 1 :
            stream_hdlr = logging.StreamHandler(sys.stdout);
            stream_hdlr.setFormatter(hd_fm);
            logger.addHandler(stream_hdlr);
    
        
    except Exception, e:
        print "init log failed %s" % str(e); 
        logger = None        
       
    return logger;
