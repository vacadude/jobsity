import csv, sqlite3
import subprocess
import sys
import pandas as pd
import geopandas as gpd
import dateutil
import shapely

import createdb

#get which file to load
try:
  filepath = sys.argv[1]
  print("Argumento exitoso")
except:
  filepath = 'trips.csv'
  print("Argumento no exitoso")

#create the db and tables in sqlite
createdb.createdb()

#load the data into a table
from pathlib import Path
db_name = Path('trips.db').resolve()
csv_file = Path(filepath).resolve()
result = subprocess.run(['sqlite3',
                         str(db_name),
                         '-cmd',
                         '.mode csv',
                         '.import --skip 1 ' + str(csv_file).replace('\\','\\\\')
                                 +' trips'],
                        capture_output=True)


con = sqlite3.connect('trips.db')
cur = con.cursor()

for row in con.execute("SELECT count(1) FROM trips"):
                        print(row)

fetch = con.execute("SELECT * FROM trips")
df = pd.DataFrame(fetch.fetchall())
df[3] = pd.to_datetime(df[3])
print(df.head())

df.groupby(pd.Grouper(key=3, freq='h'))
print(df.head())

#for row2 in con.execute("SELECT * FROM trips"):
#                        print(row2[1])
#
 #                       gdf = gpd.GeoDataFrame(row2, geometry=row2[1])
  #                      print(gdf.head())


#con.execute("INSERT INTO TRIPS SELECT region, origin_coord, destination_coord, datetime, datasource FROM trips")

df['datetime'] = df['datetime'].apply(dateutil.parser.parse, dayfirst=True)

#grouped = df.groupby(pd.Grouper(key="datetime", freq='h'))["datetime"].count()
#print(grouped.head())

df['similar_date'] = df.groupby(pd.Grouper(key="datetime", freq='1h'))["origin_coord"].transform("size")
print(df)

#for item in df['datetime'].resample('1h', kind='period'):
#    print(item)


#gdf = gpd.GeoDataFrame(data=df, 
#                       geometry=data['origin_coord']
#                       .apply(shapely.wkt.loads))
#df['origin_coord'] = gpd.GeoDataFrame(data=data, 
#                       geometry=data['origin_coord']
#                       .apply(shapely.wkt.loads))
#print(df.head())


#step = 0.2
#df['origin_lat'] = df['origin_coord'].apply(lambda p: p.x)
#df['origin_lont'] = df['origin_coord'].apply(lambda p: p.y)
#print(df.head())

#df["latBin"] = (df.Latitude // step) * step
#df["lonBin"] = (df.Longitude // step) * step
#groups = df.groupby(["latBin", "lonBin"])

con.commit()
con.close()