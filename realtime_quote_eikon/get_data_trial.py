import eikon as ek
import pandas as pd
import numpy as np

ek.set_app_key('166a7ffcef9b411ba878d7145ca2f55c78aa4b02')
list_ = ['0#IBM*.U','0#SPY*.U']
fields = ['CF_EXCHANGE','CF_DATE','CF_TIME','CF_NAME', 'PUTCALLIND', 'STRIKE_PRC','EXPIR_DATE','CF_LAST', 'TR_BIDPRICE','TR_ASKPRICE','IMP_VOLT', 'OPINT_1','CF_VOLUME']
option_chain,err = ek.get_data('0#SPY*.U', fields)