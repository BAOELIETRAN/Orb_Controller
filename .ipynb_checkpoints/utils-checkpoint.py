#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
from logging.handlers import RotatingFileHandler

#config logging setting for the app
#allow it to output logs to both the console and a file
def setup_logging(log_level):
    #if the loglevel is not provided --> log level will become WARNING
    console_loglevel = log_level or logging.WARNING
    #set up format for the console log:
    console_logformat = "[%(levelname)-8s] %(name)-30s : %(message)s"
    
    file_loglevel = log_level or logging.WARNING
    file_logformat = "%(asctime)-8s %(name)-30s %(levelname)-8s %(message)s"
    
    root_logger = logging.getLogger()
    
    file_handler = RotatingFileHandler(
        "Orb_controller.log",
        mode="a",  # append
        maxBytes=0.5 * 1000 * 1000,  # 512kB
        encoding="utf8",
        backupCount=5,  # once it hits 2.5MB total, start removing logs.
    )
    file_handler.setLevel(file_loglevel)      #set loglevel
    file_formatter = logging.Formatter(file_logformat)
    file_handler.setFormatter(file_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_loglevel) #set loglevel
    console_formatter = logging.Formatter(console_logformat)
    #tell the console_handler to use this format
    console_handler.setFormatter(console_formatter)
    
    #add the handlers to the root logger
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # suppress some of the overly verbose logs
    logging.getLogger("sacn").setLevel(logging.WARNING)
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.getLogger("zeroconf").setLevel(logging.WARNING)
    
    global _LOGGER
    _LOGGER = logging.getLogger(__name__)

