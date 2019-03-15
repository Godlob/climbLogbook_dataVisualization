import pandas as pd
import sqlite3
import sqlalchemy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pygal_maps_world.maps import World

'''
database.sqlite
Table list:
    ascent
    grade
    method
    user
'''
data = sqlite3.connect('database.sqlite')
cur = data.cursor()
query = cur.execute('select ascent.year, ascent.name, ascent.crag, ascent.sector, ascent.climb_type, ascent.country, grade.fra_routes from ascent, grade where ascent.grade_id = grade.id')
cols = [column[0] for column in query.description]
df = pd.DataFrame.from_records(data=query.fetchall(), columns = cols)
#==================================================================
# NaN and bad data handling
df = df.replace({
    'country':['','none'], 
    'fra_routes': '-' ,   
},{
    'country':np.NaN,
    'fra_routes': np.NaN,   
})
df = df.replace({
    'fra_routes' : ['8c/+','8c+/9a']
},{
    'fra_routes': '8c+'
})
#===============================================================
#grade vs route
#list to sort grade
gradesort = ['2','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6a+','6b','6b+','6c','6c+',
        '7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+','9a','9a+','9b','9b+','9c']
gradesort0 = ['2','3a','3b','3c','4a','4b','4c','5a','5b','5c','6a','6a+','6b','6b+','6c','6c+',
        '7a','7a+','7b','7b+','7c','7c+','8a','8a+','8b','8b+','8c','8c+','9a','9a+','9b','9b+']
df = df.dropna(subset =['country'])
df = df.drop_duplicates(subset=['name','crag'], keep='first')
gradecount = pd.Series(df['fra_routes'].value_counts())
gradecount = gradecount.reindex(index=gradesort)
plt.figure('figure 1: grade vs route chart', figsize=(12,12))
gradecount.plot(kind='bar')
plt.title('Grade vs Number of Routes')
plt.xlabel('Grade')
plt.ylabel('Available Route')
# plt.yticks(np.arange(0,550000, step = 50000))
plt.grid(True)
#===================================================================
#country vs route
country = df['country'].value_counts()
country = country.loc[country>1000] #have to change to 1000

plt.figure('figure 2: Number of route vs country', figsize=(12,12))
country.plot(kind='bar')
plt.title('Routes vs Country')
plt.grid(True)
plt.xlabel('Country')
plt.ylabel('Routes')
#=====================================================================
# PYGAL MAPPING OF COUNTRY VS ROUTE
countrylist = list(df['country'].unique())
countrylist.remove('ABW')
countrylist.remove('GIB')
countrylist.remove('MSR')
countrylist.remove('ATF')
countrylist.remove('KIR')
countrylist.remove('FLK')
countrylist.remove('VGB')
countrylist.remove('BMU')
countrylist.remove('WSM')
countrylist.remove('AIA')
countrylist.remove('MTQ')
countrylist.remove('ARE')
countrylist.remove('FRO')
countrylist.remove('CYM')
countrylist.remove('NCL')
countrylist.remove('KNA')
countrylist.remove('BHS')
countrylist.remove('SGS')
countrylist.remove('MNP')
countrylist.remove('BRB')
countrylist.remove('PCN')
countrylist.remove('FJI')
countrylist.remove('ASM')
countrylist.remove('BVT')
countrylist.remove('QAT')
countrylist.remove('PYF')
countrylist.remove('IOT')
countrylist.remove('GLP')
pygalList = ['th','se','au','no','fr','lu','es','be','us','it', 'at','za','nz','de',
    'ca','gb','pl','si','in','hu','hr','co','ch','cz','fi','pt','mx','gr',
    'hk', 'sk','br', 'rs', 'bg','nl','ua','il','ma','jp', 'tr', 'ro', 'ie',
    'cn', 'vn', 'eg', 'sd', 'et', 'zw', 'pe', 'my', 'cl', 've', 'il', 'ru', 'ad','tw',
    'bo', 'ar','ir', 'np', 'cu', 'dk', 're', 'mt', 'mk', 'kr', 'al', 'ke', 'md',
    'pk', 'na', 'uy', 'om', 'la', 'gf', 'hn', 'ml', 'ph', 'mk', 'sv', 'cr',
    'gu', 'mc', 'ht', 'gt', 'ee', 'ec','tj','me', 'ba', 'kg', 'cy', 'id', 'jo', 
    'dj','cv', 'sc', 'lt', 'sm', 'sz', 'kz',
    'sy', 'mo', 'tl', 'pr', 'bw', 'mn', 'do', 'ge', 'gl', 'lv', 'kp',
    'am', 'lb', 'mw', 'ao', 'ye', 'ug','pa', 'lk', 'az', 'so', 'sg', 'li',
    'gh', 'ng','ga', 'sa','by','uz', 'gm', 
    'aq', 'bh', 'tz', 'ci', 'sl', 'sr', 'tm', 'kh', 'mm', 'jm',
    'gn', 'bj', 'mv', 'rw', 'st'
]
dfmap = df.country.replace(countrylist, pygalList)
dfmap = dfmap[dfmap.isin(pygalList)]
mappingDict = dict(dfmap.value_counts())
#============================================================================
#World map charting
wmChart = World()
wmChart.title = 'Number of Climbing Routes in Each Country According to 8a.nu Log Book'
wmChart.add('Number of Routes',mappingDict)
wmChart.render_to_file('routemap.svg')
#=================================================================================
#Number of grades in each country
#Split country into 3 groups with >100k route , with>2.5k route & country with less route
country1 = country.loc[country>25000]
country1 = list(country1.index)
country2 = country.loc[country.between(5000,25000)]
country2 = list(country2.index)
country3 = country.loc[country<5000]
country3 = list(country3.index)
filtered1 = df[df['country'].isin(country1)]
#==========================================================================
#Heatmap of route grades & country
plt.figure('figure 3: Available routes by grade in each country')
filtered1 = pd.DataFrame(filtered1[['country','fra_routes']])
filtered1x = pd.crosstab(filtered1['country'],filtered1['fra_routes'])
plt.title('Route grade on country with more than 25,000 routes')
sns.heatmap(filtered1x, cmap='RdBu_r', xticklabels= gradesort, robust=True)
plt.xlabel('Grade')

plt.figure('figure 4: Available routes by grade in each country')
filtered2 = df[df['country'].isin(country2)]
filtered2 = pd.DataFrame(filtered2[['country','fra_routes']])
filtered2x = pd.crosstab(filtered2['country'],filtered2['fra_routes'])
sns.heatmap(filtered2x, cmap='RdBu_r',xticklabels= gradesort, robust=True)
plt.xlabel('Grade')
plt.ylabel('Country')
# plt.xticks(labels=gradesort)
plt.title('Route grade on country with more than 5000 routes')
plt.xlabel('Grade')

plt.figure('figure 5: Available routes by grade in each country')
filtered3 = df[df['country'].isin(country3)]
filtered3 = pd.DataFrame(filtered3[['country','fra_routes']])
filtered3x = pd.crosstab(filtered3['country'],filtered3['fra_routes'])
sns.heatmap(filtered3x, cmap='RdBu_r', xticklabels=gradesort0, robust=True)
plt.title('Route grade on country with less than 5000 routes')
plt.xlabel('Grade')

#=======================================================
#Top crags with many routes. (heatmap crag vs route & table of crag, country, and num of route)
cragsum = df['crag'].value_counts()
cragsum = cragsum.loc[cragsum>2000]
cragfilter = list(cragsum.index)
cragticks = np.array('cragfilter')
dfcrag = df[df['crag'].isin(cragfilter)]
dfcrag = pd.DataFrame(dfcrag[['crag','fra_routes']])
dfcragx = pd.crosstab(dfcrag['crag'],df['fra_routes'])

plt.figure('figure 6: Crags with many routes')
sns.heatmap(dfcragx, cmap='RdBu_r', xticklabels=gradesort0, robust=True)
plt.title('Crags With Most Routes')
plt.xlabel('Grade')
# print(len(cragfilter)) == 49
plt.yticks(ticks=np.arange(49), labels=cragfilter)

#=================================================
#show route data in SEA country
sea = ['THA', 'VNM', 'LAO', 'PHL', 'IDN','SGP','MYS']
dfsea = df[df.country.isin(sea)]
dfsea = dfsea['country'].value_counts()
plt.figure('Figure 7: Country in South East Asia')
plt.title('Number of Routes on Country in South East Asia')
plt.xlabel('Country')
plt.ylabel('Number of Routes')
dfsea.plot(kind='bar')
plt.show()