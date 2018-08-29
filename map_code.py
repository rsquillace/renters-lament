from descartes import PolygonPatch
import geopandas as gpd
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon as mpl_Polygon
from matplotlib.collections import PatchCollection

shp_path = r'tl_2010_53_zcta510.shp'

df_map_elements = gpd.GeoDataFrame.from_file(shp_path)

####################################################
########## THE LOL WUT ZONE ########################
df_map_elements["mpl_polygon"] = np.nan
df_map_elements['mpl_polygon'] = df_map_elements['mpl_polygon'].astype(object)
for self_index, self_row_df in df_map_elements.iterrows():
    #print(self_row_df)
    m_polygon = self_row_df['geometry']
    poly=[]
    if m_polygon.geom_type == 'MultiPolygon':
        for pol in m_polygon:
            poly.append(PolygonPatch(pol))
    else:
        poly.append(PolygonPatch(m_polygon))
    df_map_elements.set_value(self_index, 'mpl_polygon',
        (
            poly,
            # Specific zipcode for polygon
            self_row_df['ZCTA5CE10'],
            self_row_df['INTPTLAT10'],
            self_row_df['INTPTLON10']
        )
    )
###################################################

dict_mapindex_mpl_polygon = df_map_elements['mpl_polygon'].to_dict()

fig, ax = plt.subplots(figsize=(10, 8))

x_min = -122.46
x_max = -122.14
y_min = 47.5
y_max = 47.8

for c_l ,patches in dict_mapindex_mpl_polygon.items():
    color_ree = 'white'
    zippy = patches[1]

    ##################################################################################
    ##################################################################################
    # Change m2011 to change the industry and year, everything else should be the same
    ##################################################################################
    ##################################################################################
    if (len(m2011[m2011['zipcode'] == zippy]['affordable'].values) > 0):
        if(m2011[m2011['zipcode'] == zippy]['affordable'].values[0]):
            color_ree = 'green'
        else:
            color_ree = 'red'
    p = PatchCollection(patches[0],color=color_ree,lw=.3,edgecolor='k',label='fdlfj')
    ax.add_collection(p)
#     print(float(patches[3]))
#     print(float(patches[2]))
#     print(patches[1])
    x_coord = float(patches[3])
    y_coord = float(patches[2])
    if (x_coord > x_min and x_coord < x_max and y_coord > y_min and y_coord < y_max):
        ax.text(x_coord, y_coord,str(patches[1]), fontsize=10, horizontalalignment='center')

plt.axis([x_min, x_max, y_min, y_max])

plt.show()
