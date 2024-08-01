#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
# import import_ipynb
import utils
from args import Args
import graph

args = Args()
_LOGGER = logging.getLogger(__name__)

def main():
    utils.setup_logging(logging.INFO)

    args.parse_args()
    _LOGGER.info(f"args are {args.args}")

    graph.display(args)

if __name__ == '__main__':
    main()

