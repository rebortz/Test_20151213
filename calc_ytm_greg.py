
# coding: utf-8

# In[7]:

import pandas as pd
from pandas import *
import pylab as plt
from pylab import *
import numpy as np
import csv as csv
from scipy.optimize import newton


# In[8]:

# The following function calculate the (present value-discounted value) of the bond:
#http://pages.stern.nyu.edu/~eelton/debt_inst_class/YTM.pdf - see page 5. 
def pv_bond(ytm, first_tau, cp_no, coupon_rate, price, rdp_price,freq):
    if cp_no<1:
        fv=price-(rdp_price+(coupon_rate*rdp_price/freq))/((1+ytm/freq)**first_tau)
    else:
        dv=0
        for i in range(1,cp_no):
            dv=dv+(coupon_rate*rdp_price/freq)/((1+ytm/freq)**(i-1))
        
        dv=dv/((1+ytm/freq)**first_tau)
        
        fv=price-(rdp_price/((1+ytm/freq)**((cp_no-1)+first_tau))+dv)
    return fv

def calc_yield(trd_date,mat_date,coupon_rate,price,rdp_price,freq):
    # first determine how many coupon payments
    # freq= 2(semi-annual), 1(annual)
    trd_date=to_datetime(trd_date)

    mat_date=to_datetime(mat_date)
    period=mat_date-trd_date

    ttm=relativedelta(mat_date,trd_date)
    tau=(ttm.years*12+ttm.months)
    # Number of coupon payments:
    cp_no=tau/(12/freq)+1
    
    if cp_no>=1:
        cp_date={cp_no:mat_date}
        for i in range(1,cp_no):
            d={cp_no-i: mat_date+relativedelta(months=-6*i)}
            cp_date.update(d)
    else:
        first_ttm=relativedelta(cp_date[1],trd_date)
    
    first_ttm=relativedelta(cp_date[1],trd_date)
    first_tau=(first_ttm.months+1.0*first_ttm.days/30)/(12/freq)

    # Use Newton method to iteratively calculate the ytm
    
    # Use the coupon rate as the starting point
    x0=((coupon_rate)*rdp_price/freq)/price

    ytm=newton(pv_bond,x0,args=(first_tau, cp_no, coupon_rate, price, rdp_price,freq),maxiter=100)
    return ytm


# In[9]:

# An Example
coupon_rate=0.0675
price=106.5
rdp_price=100
freq=2

trd_date=to_datetime('20130715')
trd_date.month

mat_date=to_datetime('20211215')
period=mat_date-trd_date
print calc_yield(trd_date,mat_date,coupon_rate,price,rdp_price,freq)

