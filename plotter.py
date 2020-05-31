import numpy as np
import pandas as pd
import folium as folium

data=pd.read_csv('F1-Calendar\GPS_Co-ordinates.csv')

#print(data)
data_reduced=list(zip(data.Race_name, data.Latitude, data.Longitude))

#print(data_reduced)
#map_new=folium.Map(location=[-37.849209, 144.971816], zoom_start=2)
#trigger=0
for x in data_reduced:
    #trigger+=1
    #if(trigger<=13):
        folium.Marker(location=[x[1],x[2]], popup=x[0], icon=folium.Icon(color='blue', icon='info-sign'), radius=8).add_to(map_new)
    #elif(trigger>13):
        #folium.Marker(location=[x[1],x[2]], popup=x[0], icon=folium.Icon(color='red', icon='info-sign'), radius=8).add_to(map_new)

#map_new.save('map.html')
map_new
