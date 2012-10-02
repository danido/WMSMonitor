#!/usr/bin/python

def f_metric(value,limit,metricflag):
    '''This function returns in output a monotone positive metric normalized to domain (0,1) 
       value is the current realization of the considered variable (ex.Cpu Load average)
       limit is the user defined limit for the considered variable triggering drain limiter
       metricflag is a flag to choose the mapping function= 0-linear, 1-pseudoexp'''

    value = float(value)
#    print "value is \t", value, "\n"
    limit = float(limit)
#    print "limit is \t", limit, "\n"

    #Initializing logger
    if value>=(limit-0.0001):
	    metric=1
    else:
	    if metricflag==0:
	       metric = value / limit
	    else:
  	       metric = value / ((limit - 1) * (limit - value))
#	       print "metric is \t", metric, "\n"

    return metric
