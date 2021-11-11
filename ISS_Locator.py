#%%
import requests
from datetime import datetime,timedelta


#%%
def get_unix_time(inp_datetime, days=None, seconds=None, minutes=None, hours=None, duration=None):

    date_format = datetime.strptime(inp_datetime, "%d/%m/%Y %H:%M")

    # get ten minutes before and after input datetime (for an hour)
    hour_before = [date_format-timedelta(minutes=10*i) for i in range((duration//minutes),0,-1)]
    hour_after = [date_format+timedelta(minutes=10*i) for i in range(1,(duration//minutes)+1)]  

    # convert datetime to UNIX timestamp
    hour_before.append(date_format)
    dateTime = hour_before + hour_after
    unix_time = list(map(lambda x: int(datetime.timestamp(x)), dateTime))

    return unix_time


#%%
def get_iss_location(timestamp):
    # get ISS location
    api = 'https://api.wheretheiss.at/v1/satellites/25544/positions?timestamps={dt}&units=miles'.format(dt=','.join(map(str,timestamp)))
    request = requests.get(api).json()

    # extract timestamp, latitude and longitude
    location = [{key: request[i][key] for key in ['timestamp','latitude','longitude']} for i in range(len(request))]

    return location


#%%
def display_iss_location(locations):
    for i in range(len(locations)):
        dt = datetime.fromtimestamp(locations[i]['timestamp']).strftime('%d/%m/%Y %I:%M%p (UTC +0)')
        loc = (locations[i]['latitude'],locations[i]['longitude'])

        print("{}. {} - Coordinates: {}".format(i+1,dt,loc))


#%%
date_example = input('Enter date and time (DD/MM/YYYY HH:MM): ')
# date_example = "23/07/2021 06:51"
dateTimes = get_unix_time(date_example, minutes=10, duration=60) # duration in minutes 
req = get_iss_location(dateTimes)
display_iss_location(req)

