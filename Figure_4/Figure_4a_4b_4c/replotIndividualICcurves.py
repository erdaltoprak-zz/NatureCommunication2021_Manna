import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
from Colors import doseresponse, tmpcolor, v041color, ic50erdal
df=pd.read_csv('Data_Restructured_NoBlank_02_04_2020.csv')
colordict=dict(TMP=tmpcolor, V041=v041color)
fig,ax= plt.subplots(4,5,sharey=True, sharex=True)
sns.set_style('ticks')
sns.despine()
c=0
for line in sorted(np.random.randint(0,661,20)):
    x=df.columns[-14:].astype(np.float)
    y=df.iloc[line,-14:].values
    xfit=np.logspace(np.log10(x.min()),np.log10(x.max())*1.5, 100)
    fitparams=np.load(glob('Individual_Hill_Fit_Parameters_hVar/'+str(line)+'-*'+'.npz')[0])
    yfit=doseresponse(xfit, *fitparams['params'])
    fitparams2 = np.load(glob('Erdal_Hill_Fit_Parameters/' + str(line) + '-*' + '.npz')[0])
    yfit2 = ic50erdal(xfit, *fitparams2['params'])
    row,col= (c//len(ax[0]), c%(len(ax[0])))
    cax=ax[row,col]
    cax.semilogx(x,y,'-o',color=colordict[df['EvolvedIn'][line]])
    cax.semilogx(xfit, yfit, '-.r')
    cax.semilogx(xfit, yfit2, ':k')
    cax.semilogx(fitparams2['params'][1], ic50erdal(fitparams2['params'][1], *fitparams2['params']),'^r')
    cax.semilogx(fitparams2['params'][1]*(19**(1/fitparams2['params'][2])),
                 ic50erdal(fitparams2['params'][1]*(19**(1/fitparams2['params'][2])), *fitparams2['params']), 'vr')
    title= df['EvolvedIn'][line]+'-'+\
           str(df['Culture#'][line])+'-'+\
           str(df['Day#'][line])
    cax.set_title(title, y=0.95)
    if row==3:
        cax.set_xlabel('[Drug] (µg/mL)')
    else:
        cax.set_xlabel('')
    if col==0:
        cax.set_ylabel('O.D. (a.u.)')
    else:
        cax.set_ylabel('')

    c+=1
fig.tight_layout(pad=.9)

