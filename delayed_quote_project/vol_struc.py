from opx_chain import options_chain
import matplotlib.pyplot as plt
def term_structure(sym):
    opx = options_chain(sym)
    return opx
opx = term_structure("AAPL")

for i in list(opx.exDate.unique()):
    plt.plot(opx[opx.exDate == i].strike, opx[opx.exDate == i].IV)
    #plt.legend(opx.exDate)