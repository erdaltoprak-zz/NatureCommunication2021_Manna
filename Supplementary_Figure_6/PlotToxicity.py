import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import v041color, tmpcolor, change_width

df=pd.read_excel('Cell_Titer_Glo_summary_for_ET_and_MM_TMP_V-041.xlsx','Summary')

fig,ax=plt.subplots(2,2, sharex=True, sharey=True)
sns.set_style('ticks')
sns.despine()
legends=[False,False,'brief',False]
c=0
for expTime in [24, 48]:
    for celltype in ['Dividing','Confluent']:
        cax=ax[c//len(ax[0]), c%len(ax[0])]
        sns.barplot(x='Concentration',y='Growth',hue='Drug',
                    hue_order=['TMP','4\'-DTMP'], ci='sd',
                    palette=[tmpcolor, v041color], capsize=.05,
                    errwidth=1.5,edgecolor='k', errcolor='k',
                    data=df.loc[(df.CellType==celltype) &
                                (df.Time==expTime), :], ax=cax)
        change_width(cax, 0.35)
        cax.set_ylim(0,120)
        if c==2:
            handles, labels=cax.get_legend_handles_labels()
            cax.legend(handles,labels,ncol=2,loc=1,frameon=False, bbox_to_anchor=(.8,1.1))
        else:
            cax.get_legend().remove()
        if c%2==1:
            cax.set_ylabel('')

        if c//2==0:
            cax.set_xlabel('')
        else:
            cax.set_xlabel('[Drug] (µM)')

        c+=1
ax[0,0].set_title('Dividing Cells', y=1.1, fontweight='bold', horizontalalignment='center',fontsize=14)
ax[0,1].set_title('Confluent Cells', y=1.1 , fontweight='bold', horizontalalignment='center',fontsize=14)
ax[0,0].set_ylabel('ATP content at 24h\n(relative to DMSO)')
ax[1,0].set_ylabel('ATP content at 48h\n(relative to DMSO)')
fig.set_size_inches(7,5)
fig.tight_layout(pad=1)
# fig.savefig('Toxicity-Data-24-48h-Dividing-Confluent.pdf',dpi=600, transparent=True)