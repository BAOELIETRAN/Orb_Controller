#!/usr/bin/env python
# coding: utf-8

# In[1]:


import logging
import utils
from args import Args
import graph

args = Args()
_LOGGER = logging.getLogger(__name__)

def main():
    utils.setup_logging(logging.INFO)

    args.parse_args()
    _LOGGER.info(f"args are {args.args}")

    graph.get_information(args)
    graph.get_ping_information(args)
    
    if args.args.graph == False and args.args.table == True:
        graph.display_table(args)
    elif args.args.graph == True and args.args.table == True:
        graph.display(args)
        graph.display_table(args)
    else:
        graph.display(args)

    graph.warning(args)

if __name__ == '__main__':
    main()


# %%
