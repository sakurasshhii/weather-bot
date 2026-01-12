import openmeteo_requests

from app.bot.lexic import coordinates


async def get_weather(city: str):
    return 'some value'
    # openmeteo = openmeteo_requests.AsyncClient()

    # # all required weather variables are listed below
    # # The order of variables in hourly or daily is important to assign them correctly below
    # url = "https://api.open-meteo.com/v1/forecast"
    # params = {
    #     "latitude": coordinates[city]['latitude'],
    #     "longitude": coordinates[city]['longitude'],
    #     "hourly": ["temperature_2m", "precipitation", "wind_speed_10m"],
    #     "current": ["temperature_2m", "relative_humidity_2m"],
    #     "timezone": "auto"
    # }
    # print('inside of func')
    # responses = await openmeteo.weather_api(url, params=params)

    # # Process first location. Add a for-loop for multiple locations or weather models
    # response = responses[0]
    # print('response getted')
    # print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation: {response.Elevation()} m asl")
    # print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process current data. The order of variables needs to be the same as requested.
    # current = response.Current()
    # current_temperature_2m = current.Variables(0).Value()
    # current_relative_humidity_2m = current.Variables(1).Value()

    # print(f"Current time: {current.Time()}")
    # print(f"Current temperature_2m: {current_temperature_2m}")
    # print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")

    # return response
