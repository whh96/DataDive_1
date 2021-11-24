import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import circlify as circlify
from pprint import pprint as pp

# reading in datasets
df = pd.read_excel('HDI_HDIcomponents.xlsx', index_col=0)
df2 = pd.read_excel('WHR2020.xlsx', index_col=0)

# merging datasets
df3 =pd.merge(df, df2, on = "country")

df4 = pd.read_excel('HDI_HDIcomponents.xlsx', index_col=0)

# we need to get a 
# print(df3.head())

columns = ['iso3_x', 'HDIrank']
GDP_df = pd.DataFrame(df3, columns=columns)
# print(GDP_df.head(50))

circles = circlify.circlify(
    GDP_df['HDIrank'].tolist(), 
    show_enclosure=False, 
    target_enclosure=circlify.Circle(x=0, y=0, r=1)
)

fig, ax = plt.subplots(figsize=(5,5))
# Remove axes
ax.axis('off')
ax.set_title('GNIpc')
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

labels = GDP_df['iso3_x']

# print circles
#for circle in circles:
#    x, y, r = circle
#    ax.add_patch(plt.Circle((x, y), r, alpha=0.2, linewidth=2, fill=False))

'''
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
'''

# you need to use https://stackoverflow.com/questions/55910004/get-continent-name-from-country-using-pycountry
# to build a for loop that adds a certain variable amount to 1 of the continents. 
# from that, you can build a better bubble chart. Start with HDI and then try mean years of schooling