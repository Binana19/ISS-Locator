'''
Author : Sabrina Leong Tong Tao 
Date modified: 12/11/2021

** NeXT Graduate Programme Assessment **
Task: Getting the location of the ISS at a specific time

The following program get users to enter a past date and time and
receive the location coordinates the ISS was over at that moment, as well as its 
location every ten minutes before and after that for an hour.
'''

# import required modules 
import sys
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from itertools import chain
from mpl_toolkits.basemap import Basemap


def draw_map(m, scale=0.2):
    """
    Drawing world map.
    Code referenced from https://jakevdp.github.io/PythonDataScienceHandbook/04.13-geographic-data-with-basemap.html
    """
    # draw a shaded-relief image
    m.shadedrelief(scale=scale)
    
    # lats and longs are returned as a dictionary
    lats = m.drawparallels(np.linspace(-90, 90, 13))
    lons = m.drawmeridians(np.linspace(-180, 180, 13))

    # keys contain the plt.Line2D instances
    lat_lines = chain(*(tup[1][0] for tup in lats.items()))
    lon_lines = chain(*(tup[1][0] for tup in lons.items()))
    all_lines = chain(lat_lines, lon_lines)
    
    # cycle through these lines and set the desired style
    for line in all_lines:
        line.set(linestyle='-', alpha=0.3, color='w')


def get_unix_time(inp_datetime, minutes=10, duration=60):
    """
    Get datetime of specified interval (in minutes) from input for desired duration and convert the datetimes
    to UNIX timestamp.

    Arguments:      inp_datetime = user input datetime in DD/MM/YYYY HH:MM - 24HR format
                    minutes      = specified interval, 10 minutes by default
                    duration     = specified duration, 60 minutes by default
    Returns: a list of UNIX timestamp 
    """

    date_format = datetime.strptime(inp_datetime, "%d/%m/%Y %H:%M")

    # get ten minutes before and after input datetime (for an hour)
    hour_before = [date_format-timedelta(minutes=10*i) for i in range((duration//minutes),0,-1)]
    hour_after = [date_format+timedelta(minutes=10*i) for i in range(1,(duration//minutes)+1)]  

    # convert datetime to UNIX timestamp
    hour_before.append(date_format)
    dateTime = hour_before + hour_after
    unix_time = list(map(lambda x: int(datetime.timestamp(x)), dateTime))

    return unix_time


def get_iss_location(timestamp):
    """
    Get coordinates of the location of ISS.

    Arguments:      timestamp = list of UNIX timestamp 
    Returns: a list of ISS's location 
    """

    # get ISS location
    api = 'https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={dt}&units=miles'.format(dt=','.join(map(str,timestamp)))
    request = requests.get(api).json()

    # extract timestamp, latitude and longitude
    location = [{key: request[i][key] for key in ['timestamp','latitude','longitude']} for i in range(len(request))]

    return location


def display_iss_location(locations):
    """
    Display location of ISS.

    Arguments:      locations = a list of coordinates  
    """

    print("\n{} ISS Location {}".format('='*33,'='*33))

    lon = []
    lat = []

    for i in range(len(locations)):
        dt = datetime.fromtimestamp(locations[i]['timestamp']).strftime('%d/%m/%Y %I:%M%p (UTC +0)')
        coord = (locations[i]['latitude'],locations[i]['longitude'])
        lon.append(coord[1])
        lat.append(coord[0])

        print("{}. {} - Coordinates: {}".format(i+1,dt,coord))

    # Visualize ISS location on Cylindrical Projection 
    fig = plt.figure(figsize=(8, 6), edgecolor='w')
    m = Basemap(projection='cyl', resolution=None,
                llcrnrlat=-90, urcrnrlat=90,
                llcrnrlon=-180, urcrnrlon=180, )
    draw_map(m)

    # convert to map projection coords - can be scalars, lists or numpy arrays
    xpt,ypt = m(lon,lat)
    # convert back to lat/lon
    lonpt, latpt = m(xpt,ypt,inverse=True)
    m.plot(xpt,ypt,'bo')  # plot a blue dot 

    # label data points
    for i in range(len(lonpt)):
        dt = datetime.fromtimestamp(locations[i]['timestamp']).strftime('%d/%m/%Y %H:%M')
        plt.text(xpt[i]-2,ypt[i]+2,'%s\n(%3.1fN,%5.1fW)' % (dt,latpt[i],lonpt[i]),fontsize=7)

    plt.show()

            

if __name__ == "__main__":
    
    # while True:
    #     date_example = input('\nEnter date and time (DD/MM/YYYY HH:MM - 24HR format): ') # e.g "23/07/2021 06:51"
    #     valid = True
    #     try:
    #         datetime.strptime(date_example, "%d/%m/%Y %H:%M")

    #     except ValueError:
    #         valid = False

    #     if valid:
    #         dateTimes = get_unix_time(date_example, minutes=10, duration=60) # duration in minutes 
    #         req = get_iss_location(dateTimes)
    #         display_iss_location(req)
    #         sys.exit()
            
    #     else: 
    #         print('Invalid datetime, please enter again')

    date_example = "23/07/2021 06:51"
    dateTimes = get_unix_time(date_example, minutes=10, duration=60) # duration in minutes 
    req = get_iss_location(dateTimes)
    display_iss_location(req)
    
