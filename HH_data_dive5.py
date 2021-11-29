import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import pycountry
import pycountry_convert as pc
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
import circlify as circlify
from pprint import pprint as pp

# reading in datasets
df = pd.read_excel('HDI_HDIcomponents.xlsx', index_col=1)
df2 = pd.read_excel('worldData.xlsx', sheet_name='data', index_col=0)

# So pycountry wouldn't work for this dataset that well so I had to manually change some of the values
# there was probably a much more efficient way to do this but oh well.
# Also, I couldn't get Timor-Leste to work with pycountry so I just omitted it. Don't tell His Excellency.
df = df.drop('TLS')
df2 =df2.drop('Timor-Leste')
df.at['BOL','country']='Bolivia'
df.at['COD', 'country'] = 'Congo'
df.at['SWZ', 'country'] = 'Eswatini'
df.at['HKG', 'country'] = 'Hong Kong'
df.at['IRN', 'country'] = 'Iran'
df.at['PRK', 'country'] = 'North Korea'
df.at['KOR', 'country'] = 'South Korea'
df.at['FSM', 'country'] = 'Micronesia'
df.at['MDA', 'country'] = 'Moldova'
df.at['TZA', 'country'] = 'Tanzania'
df.at['VEN', 'country'] = 'Venezuela'
final_df =pd.merge(df, df2, on = "country")


final_df = final_df.loc[ :,['country', 'Buddhist', 'Christian', 'Hindu', 'Muslim']]


list_of_countries = final_df['country'].tolist()

continents = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}


list_of_continents = [continents[country_alpha2_to_continent_code(country_name_to_country_alpha2(country))] for country in list_of_countries]

# make a new continent column
final_df = final_df.assign(Continent=list_of_continents)

final_df = final_df.loc[ :,['Buddhist', 'Christian', 'Hindu', 'Muslim', 'Continent']]


final_df = final_df.groupby(['Continent'])[['Buddhist', 'Christian', 'Hindu', 'Muslim']].mean().reset_index()

# I did this because circlify wouldn't label the circles correctly but this method worked.
buddhist = final_df.sort_values(by = 'Buddhist', ascending=True)
christian = final_df.sort_values(by = 'Christian', ascending=True)
hindu = final_df.sort_values(by = 'Hindu', ascending=True)
muslim = final_df.sort_values(by = 'Muslim', ascending=True)




# Change the column in final_df accordingly.
circles = circlify.circlify(
    final_df['Muslim'].tolist(), 
    show_enclosure=False, 
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

# Change the title accordingly

fig, ax = plt.subplots(figsize=(5,5))
# Remove axes
ax.axis('off')
ax.set_title('Muslim prevalence per continent')
# Find axis boundaries

lim = max(
    max(
        abs(circle.x) + circle.r,
        abs(circle.y) + circle.r,
    )
    for circle in circles
)
plt.xlim(-lim, lim)
plt.ylim(-lim, lim)

# Change the df accordingly
labels = muslim['Continent']

# print circles
for circle in circles:
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2, fill=False))


for circle, label in zip(circles, labels):
    x, y, r = circle
    ax.add_patch(plt.Circle((x, y), r, alpha=0.9, linewidth=2))
    plt.annotate(
          label, 
          (x,y ) ,
          va='center',
          ha='center'
     )



plt.show()
