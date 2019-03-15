import pandas as pd
import sqlite3
import sqlalchemy
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pygal_maps_world.maps import World

# df = pd.read_csv('tes.csv')
# listnama = list(df['nama'])
# # df = df.nama.replace(listnama,['Alpha','Bravo','Charlie','Delta','Echo'])
# listnama.remove('Andi')
# print(listnama)
# print(df.unique())
worldmap_chart = World()
worldmap_chart.title = 'Some countries'
worldmap_chart.add('',{
  'af': 14,
  'bd': 1,
  'by': 3,
  'cn': 1000,
  'gm': 9,
  'in': 1,
  'ir': 314,
  'iq': 129,
  'jp': 7,
  'kp': 6,
  'pk': 1,
  'ps': 6,
  'sa': 79,
  'so': 6,
  'sd': 5,
  'tw': 6,
  'ae': 1,
  'us': 43,
  'ye': 28
})
worldmap_chart.render_to_file('map.svg')
# worldmap_chart.render_in_browser()