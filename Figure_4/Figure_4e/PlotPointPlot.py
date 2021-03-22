import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Colors import change_width,  tmpcolor, v041color, colorsall

markers=['x','o','s','^','v','+','<','s','o','>']
hueorder=['c-35t','L28R','A26T','W30C/G/R','I94L','F153S/V','D27E','P21L/S/Q','R98P','Y151S']
pal=[colorsall[h] for h in hueorder]
df=pd.read_excel('Day21_MajorMutations.xlsx','Summary')
fig,ax=plt.subplots()
sns.set_style('ticks')
sns.despine()
sns.pointplot(x='Drug',y='Frequency',hue='Mutation',
              hue_order=hueorder,data=df,ax=ax,
              palette=pal, markers=markers, )
ax.set_ylim(-5,100)
ax.set_xlim(-.1,1.4)
ax.set_ylabel('Frequency at final day (%)')
ax.legend(frameon=False, loc=1)
fig.set_size_inches(6,4)
fig.tight_layout(pad=.5)
fig.savefig('FinalDayFrequencies.pdf',dpi=600,transparent=True)
fig.savefig('FinalDayFrequencies.png',dpi=600,transparent=True)

fig2, ax2 = plt.subplots()
sns.set_style('ticks')
sns.despine()
df2= df.pivot(index='Mutation', columns='Drug',values='Frequency')
df2 = df2.reset_index()
df2.loc[df2.Mutation=='R98P',['4\'-DTMP','TMP']]=[10,0.5]
df2.loc[df2.Mutation=='Y151S',['4\'-DTMP','TMP']]=[13.01,1]
sns.scatterplot('TMP','4\'-DTMP',hue='Mutation', hue_order=hueorder,
                data=df2, palette=pal, s=80, ax=ax2, edgecolor='k', legend='full')
ax2.plot([0.1, 100],[0.1, 100],'--k', alpha=.1, zorder=0)
ax2.axis('square')
ax2.set(xlim=(0,100), ylim=(0,100),
        xlabel='Frequency of Mutation in TMP (%)',
        ylabel='Frequency of Mutation in 4\'-DTMP (%)') #xscale='log', yscale='log',
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[1:],labels[1:],ncol=2, loc=2, frameon=False, bbox_to_anchor=(0,1.05))
fig2.savefig('FinalDay_Frequency_TMP_4DTMP.png', dpi=600, transparent=False)
fig2.savefig('FinalDay_Frequency_TMP_4DTMP.pdf', dpi=600, transparent=False)
