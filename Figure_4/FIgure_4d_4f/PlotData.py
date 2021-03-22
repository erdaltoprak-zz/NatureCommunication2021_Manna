import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import colorsall
def despineme(currax,left=True):
    if left:
        sns.despine(ax=currax)
    else:
        sns.despine(ax=currax,left=True)
        currax.yaxis.set_tick_params(width=0, which='both')
        currax.set_ylabel('')
    return None


colordict=colorsall
df=pd.read_excel('Representative Examples.xlsx','Sheet2')

fig,ax=plt.subplots(2,2,sharey=True, sharex=True)
sns.set_style('ticks')
kws=dict(markers=True,marker='o',markeredgecolor='k',lw=1.5,markersize=6, legend=False)

df.Frequency/=100.
df['Time (d)']+=np.random.normal(0,.5,len(df))

currax=ax[0,0]
despineme(currax,left=True)
dfnow=df.loc[df['Culture']==1,:]

palette=[colorsall[h] for h in ['A26T','L28R']]#['c','m']
sns.lineplot(x='Time (d)',y='Frequency',hue='Mutation', hue_order=['A26T','L28R'],
             data=dfnow, palette=palette,ax=currax, **kws)
for i in ['c-35t','A26T','L28R','W30R']:
    currax.plot(-5,-5,'-o',color=colordict[i],markeredgecolor='k',label=i)
currax.legend(frameon=False,loc='center right', ncol=1, bbox_to_anchor=(1.1,0.5), fontsize=8)
currax.set_xlim(-3,24)
currax.set_ylim(-.05,1.05)
currax.set_ylabel('Frequency - TMP')

currax=ax[0, 1]
despineme(currax,left=False)
dfnow=df.loc[df['Culture']==2,:]
palette=[colorsall[h] for h in ['c-35t','A26T','W30R','L28R']]#['darkgrey','c','lime','m']
sns.lineplot(x='Time (d)',y='Frequency',hue='Mutation',hue_order=['c-35t','A26T','W30R','L28R'],
             data=dfnow, palette=palette,ax=currax, **kws)

currax=ax[1, 0]
despineme(currax,left=True)
dfnow=df.loc[df['Culture']==3,:]
palette=[colorsall[h] for h in ['c-35t','P21L','W30C']]
sns.lineplot(x='Time (d)',y='Frequency',hue='Mutation',hue_order=['c-35t','P21L','W30C'],
             data=dfnow, palette=palette,ax=currax, **kws)

for i in ['c-35t','P21L','A26T','W30R','W30C','I94L','R98P']:
    currax.plot(-5,-5,'-o',color=colordict[i],markeredgecolor='k',label=i)
currax.legend(frameon=False,loc='center right', ncol=1, bbox_to_anchor=(1.1,0.5), fontsize=8)
# currax.set_title('4\'-DTMP - Culture-1' , y=.95)
currax.set_ylabel('Frequency - 4\'-DTMP')
currax=ax[1, 1]
despineme(currax,left=False)
dfnow=df.loc[df['Culture']==4,:]
palette=[colorsall[h] for h in ['c-35t','A26T','W30R','I94L','R98P']]#['darkgrey','c','lime','b','yellow']
sns.lineplot(x='Time (d)',y='Frequency',hue='Mutation',
             data=dfnow, palette=palette,ax=currax, **kws)

fig.set_size_inches(6.8,4)
fig.tight_layout(pad=1)
fig.savefig('Frequencies-Time-Representative-xNoise2.png',dpi=600, transparent=True)
fig.savefig('Frequencies-Time-Representative-xNoise2.pdf',dpi=600)

