import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import ic50erdal, ic50wiki, doseresponse
thr = 1e-15
x=np.logspace(-1,5,250)
fig,ax=plt.subplots(3,1,sharex=True,sharey=True)
sns.set_style('ticks')
sns.despine()
for h in range(1,6):
    yDR=doseresponse(x,1,100,h)
    yE1=ic50erdal(x,1, 100, h)
    yE2=ic50wiki(x, 1, 100, h)
    print(sum(yDR-yE1<thr),sum(yE2-yE1<thr),sum(yDR-yE2<thr))
    ax[0].semilogx(x,yDR,label='h='+str(h))
    ax[1].semilogx(x, yE1, label='h=' + str(h))
    ax[2].semilogx(x, yE2, label='h=' + str(h))

ax[0].set_title('3 parameters Log-logistic fit',y=.95)
ax[1].set_title('Hill Equation from ET',y=.95)
ax[2].set_title('Hill Equation from Wikipedia',y=.95)

ax[0].text(.5,.1,'$OD = \\frac{OD_{max}}{1 + e^{h*(\log{[D]}-\log{IC_{50}})}}$', fontsize=12 )
ax[1].text(.5,.1,'$OD = OD_{max} * \\frac{IC^h_{50}}{IC^h_{50} + [D]^h}$' , fontsize=12)
ax[2].text(.5,.1,'$OD = OD_{max} * \\frac{1}{1+(\\frac{IC_{50}}{[D]})^h}}$' , fontsize=12)


for i in range(3):
    ax[i].set_ylabel('OD')
    ax[i].legend(loc=1)
ax[2].set_xlabel('[Drug]')