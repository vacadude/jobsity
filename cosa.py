import pandas as pd
import geopandas as gpd
import dateutil
import shapely


# Load data from csv file
data = pd.read_csv('trips.csv')
# Convert date from string to date times
data['datetime'] = data['datetime'].apply(dateutil.parser.parse, dayfirst=True)

#grouped = data.groupby(pd.Grouper(key="datetime", freq='h'))["datetime"].count()
#print(grouped.head())

data['similar_date'] = data.groupby(pd.Grouper(key="datetime", freq='1h'))["origin_coord"].transform("size")
print(data)

#for item in data['datetime'].resample('1h', kind='period'):
#    print(item)


#gdf = gpd.GeoDataFrame(data=data, 
#                       geometry=data['origin_coord']
#                       .apply(shapely.wkt.loads))
#data['origin_coord'] = gpd.GeoDataFrame(data=data, 
#                       geometry=data['origin_coord']
#                       .apply(shapely.wkt.loads))
#print(data.head())


#step = 0.2
#data['origin_lat'] = data['origin_coord'].apply(lambda p: p.x)
#data['origin_lont'] = data['origin_coord'].apply(lambda p: p.y)
#print(data.head())

#data["latBin"] = (data.Latitude // step) * step
#data["lonBin"] = (df.Longitude // step) * step
#groups = df.groupby(["latBin", "lonBin"])