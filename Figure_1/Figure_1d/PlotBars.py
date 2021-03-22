from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
mutdict={'c-35t':0.85,	'g-31a':0.23,	'c-15g':0.03,	'g-9a':0.18,
         'I5F':0.03,	'M20I':0.03,	'P21Q':0.10,	'P21L':0.13,
         'A26T':0.5,	'A26V':0.03,	'A26S':0.03,	'D27E':0.4,
         'L28R':0.75,	'W30R':0.43,	'W30G':0.13,	'W30C':0.23,
         'W30Y':0.1,	'I94L':0.13,	'R98P':0.1, 	'F153S':0.25,
         'F153V':0.08,	'F153L':0.03}
mutnames=list(mutdict.keys())
hashes=['//','--','++','||','//','//','--','//','//','--','||','//','//','//','||','--','++','//','//','//','--','||']
colors=[(.4, .4, .4),(.4, .4, .4),(.4, .4, .4),(.4, .4, .4),
        (0.19607843, 0.47058824, 0.74509804),(0.74509804, 0.58823529, 0.2745098 ),(1, 0, 0),(1, 0, 0),
        (0, 1, 1),(0, 1, 1),(0, 1, 1),(0, 0, 0),
        (1, 0, 1),(0, 1, 0),(0, 1, 0),(0, 1, 0),
        (0, 1, 0),(0, 0, 1),(1, 1, 0),(1.        , 0.47058824, 0.        ),
        (1.        , 0.47058824, 0.        ),(1.        , 0.47058824, 0.        )]
fig, ax = plt.subplots()
sns.set_style('ticks')
sns.despine()
c=0
for i in mutdict.keys():
    # ax.bar(c, mutdict[i],color=None, edgecolor='k', linewidth=1 )
    ax.bar(c,mutdict[i],color=colors[c],hatch=hashes[c],edgecolor='black',linewidth=1)
    c+=1
ax.set_ylim(0,1)
ax.set_yticks(np.arange(0,1.2,.2))
ax.set_ylabel('Observed Frequency')
ax.set_xlabel('Mutations Acquired')
ax.set_xticks(np.arange(c))
ax.set_xticklabels(dict(zip(mutnames,range(c))), rotation=90)
fig.set_size_inches(8,4)
fig.tight_layout(pad=.5)
fig.savefig('MutationFrequencies.pdf',dpi=600, transparent=True)
fig.savefig('MutationFrequencies.png',dpi=600, transparent=True)