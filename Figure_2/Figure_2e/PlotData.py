import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from Colors import tmpcolor, v041color, change_width, mw_v041, mw_tmp

df=pd.read_csv('IC95.csv')
df.set_index(['strain','drug'],inplace=True)
df2=df.stack().reset_index()
df2.columns=['Strain','Drug','Replica','MIC']
df2['MIC']*=1000
df2.loc[df2['Drug']=='V-041','Drug']='4\'-DTMP'

palette=[tmpcolor,v041color]
fig,ax=plt.subplots()
sns.set_style("ticks")
sns.despine()
sns.barplot(x='Strain',y='MIC',hue='Drug',
            data=df2,palette=palette,
            capsize=.05,errwidth=1.5,
            edgecolor='k',errcolor='k', ci='sd')
change_width(ax,.3)
ax.set_xticklabels(['E. coli\nMG1655','E. coli\nClinical Isolate',
                    'K. pneumoniae\nF45153','P. aeruginosa\nPAO1',
                    'S. aureus\nRN4220'],fontstyle='italic', fontsize=8, rotation=90,
                   horizontalalignment='center', verticalalignment='top')
ax.set_yscale('log')
ax.set_ylabel('IC$_{95}$ (µM)')
ax.set_xlabel('')
ax.get_legend().remove()
ax.legend(frameon=False, fontsize=7, loc=2)
ax.set_ylim(1e-1,1e3)
fig.set_size_inches(2.6,2.0)
fig.tight_layout(pad=.95)
fig.savefig('BarPlot_IC95-DifferentStrains.pdf',dpi=600)
fig.savefig('BarPlot_IC95-DifferentStrains.png',transparent=True,dpi=600)

######## Convert concentration to ug/ml ########
df2['MIC_ug']=0
df2.loc[df2.Drug=='TMP','MIC_ug']=df2.loc[df2.Drug=='TMP','MIC'] * mw_tmp * 1e-3
df2.loc[df2.Drug=="4\'-DTMP",'MIC_ug']=df2.loc[df2.Drug=="4\'-DTMP",'MIC'] * mw_v041 * 1e-3

fig,ax=plt.subplots()
sns.set_style("ticks")
sns.despine()
sns.barplot(x='Strain',y='MIC_ug',hue='Drug',
            data=df2,palette=palette,
            capsize=.05,errwidth=1.5,
            edgecolor='k',errcolor='k', ci='sd')
change_width(ax,.3)
xms = sorted([-0.35, 0.65, 1.65, 2.65, 3.65, 0.05, 1.05, 2.05, 3.05, 4.05])
c = 0
for strain in df2.Strain.unique():
    for drug in df2.Drug.unique():
        yvals = df2.loc[(df2.Strain == strain) & (df2.Drug == drug), 'MIC_ug'].values
        xvals = np.ones(len(yvals)) * xms[c] + (np.random.random(len(yvals)) - .5) * .2 + .15
        # print(strain, drug, xvals, yvals)
        ax.plot(xvals, yvals, 'o', color='k', markersize=2, alpha=.5)
        c += 1

ax.set_xticklabels(['E. coli\nMG1655','E. coli\nClinical Isolate',
                    'K. pneumoniae\nF45153','P. aeruginosa\nPAO1',
                    'S. aureus\nRN4220'],fontstyle='italic', fontsize=8, rotation=90,
                   horizontalalignment='center', verticalalignment='top')
ax.set_yscale('log')
ax.set_ylabel('IC$_{95}$ (µg/ml)')
ax.set_xlabel('')
ax.get_legend().remove()
ax.legend(frameon=False, fontsize=7, loc=2, bbox_to_anchor=(0.01, 1.05))
ax.set_ylim(1e-1,1e3)
fig.set_size_inches(2.6,2.0)
fig.tight_layout(pad=.95)
fig.savefig('BarPlot_IC95-DifferentStrains_ug_wDots.pdf',dpi=600)
fig.savefig('BarPlot_IC95-DifferentStrains_ug_wDots.png',transparent=True,dpi=600)
