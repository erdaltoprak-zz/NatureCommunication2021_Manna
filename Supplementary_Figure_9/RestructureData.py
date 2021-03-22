import pandas as pd
import numpy as np
global icx
def findICx(ODs):
    concs=ODs.index
    ODs=ODs.values
    ODthr=max(ODs)*(1-icx)
    ODbool=ODs<ODthr
    if sum(ODbool)<1:
        ICx = 6250#max(concs)
    else:
        ICx = min(concs[ODbool])
    return ICx

def parseName(name):
    if name[0]=='T':
        cultname=name+'D21'
        evolvedIn='TMP'
        measuredIn='V041'
        culturenum=int(name.replace('T',''))
    else:
        cultname=name+'D21'
        evolvedIn='V041'
        measuredIn='TMP'
        culturenum=int(name.replace('V',''))
    return cultname,evolvedIn, measuredIn, culturenum
df1=pd.read_excel('Cross_MIC_of_T1_to_T7_against_V041_24 h.xlsx','BgCorrected')
df2=pd.read_excel('Cross_MIC_of_V1_to_V8_against_TMP_24 h.xlsx','BgCorrected')

df=pd.concat([df1,df2],axis='columns').iloc[:84,:]
df['DrugConc']=[.04,.66,1.64,4.1,10.2,25.6,64,160,400,1000,1750,2500]*7
df['Replica']=[(i//12)+1 for i in range(84)]
df=df.set_index(['Replica','DrugConc']).stack().reset_index()
df.columns=['Replica','DrugConc','CultureName','OD']
ddf=df.set_index(['CultureName','Replica'])
ddf2=ddf.pivot(columns='DrugConc')
ddf2.columns=[.04,.66,1.64,4.1,10.2,25.6,64,160,400,1000,1750,2500][::-1]
ddd=ddf2[ddf2.columns[::-1]]
dfall=pd.DataFrame([],index=ddf2.index)
dfall.reset_index(inplace=True)
out =dfall['CultureName'].apply(parseName)
dfall[['Name','EvolvedIn', 'MeasuredIn', 'Culture#']] = pd.DataFrame(out.to_list(),index=dfall.index)

dfall=dfall.set_index(['CultureName','Replica'])

for icx in [0.95, 0.75, 0.5]:
    dfall['IC'+str(int(icx*100))]=ddd.apply(findICx,axis='columns')

dfFinal=pd.concat([dfall,ddd],axis='columns')
dfFinal=dfFinal.reset_index().drop(['CultureName'],axis='columns')

dfFinal.to_csv('AllDataRestructured.csv',index=False)


