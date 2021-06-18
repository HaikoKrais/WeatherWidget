# encoding: utf-8

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
import urllib.request
import json
from time import gmtime, strftime
from kivy.network.urlrequest import UrlRequest

class WeatherWidget(RelativeLayout):
    '''Shows current weather and 5 day forecast based on OpenWeatherMap API.

    Attributes:
    The attributes are bound by name to propertis in the kv file. Updating them will automatically update the displayed data in the visualisation
    
    city (StringProperty, str):
        Name of the city.
        Initially set to --.
    country (StringProperty, str):
        Country code according to ISO where the city is located in.
        Initially set to --.
    temperature (StringProperty, str):
        Current temperature.
        Initially set to --.
    humidity (StringProperty, str):
        Current humidity.
        Initially set to --.
    pressure (StringProperty, str):
        Current humidity.
        Initially set to --.
    wind_speed (StringProperty, str):
        Current wind speed.
        Initially set to --.
    wind_direction (StringProperty, str):
        Current wind direction.
        Initially set to --.
    last_update (StringProperty, str):
        Time at which the data has been updated last from OpenWeatherMap.
        Initially set to --.
    notification  (StringProperty, str):
        Error string. Shows exceptions, like no data available.
        Initially set to --.
    image_source (StringProperty, str):
        url of the icon showing the current weather conditions.
        Initially set to --.
'''

    city = StringProperty('--')
    country = StringProperty('--')
    temperature = StringProperty('--')
    humidity = StringProperty('--')
    pressure = StringProperty('--')
    image = StringProperty('--')
    wind_speed = StringProperty('--')
    wind_direction = StringProperty('--')
    last_update = StringProperty('--')
    notification = StringProperty('')
    image_source = StringProperty('')
    forecast = []
    
    def download_current_weather(self, city, *args, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&APPID=YourAPPIDGoesHere'
        UrlRequest(url = url, on_success = self.show_current_weather, on_error = self.download_error, on_progress = self.progress, chunk_size = 40960)

    def download_forecast(self, city, *args, **kwargs):
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&APPID=YourAPPIDGoesHere' 
        UrlRequest(url = url, on_success = self.show_forecast, on_error = self.download_error, on_progress = self.progress, chunk_size = 40960)

    def download_error(self, request, error):
        '''notify on error'''
        self.notification = 'data could not be downloaded'

    def progress(self, request, current_size, total_size):
        '''show progress to the user'''
        self.notification = ('Downloading data: {} bytes of {} bytes'.format(current_size, total_size))

    def show_current_weather(self, request, result):
        '''update displayed data for current weather.

        The data is stored as described in the OpenWeatherMap API.
        https://openweathermap.org/api/one-call-api?gclid=EAIaIQobChMI1bGR2-Dd6AIVxuN3Ch1sWAgGEAAYAiAAEgK6E_D_BwE
        The keys are read using the dictionary get() method because OpenWeatherMap does not always provide all data.
        Keys which are not available will be read as 'nn'

        Args:
            *args (): not used. For further development.
            **kwargs (): not used. For further development.

        Returns:
            (float): Scaled value.

        Raises:
            FileNotFoundError: Raised if no now.json file is found

        The files searched for in the folder where teh MyVisuApp.py file is located. See get_http_to_json for reference
        '''

        self.city = result.get('name','nn')
        self.country = result.get('sys').get('country','nn')
        self.temperature = '{:.0f}'.format(result.get('main').get('temp') - 273.15)
        self.humidity = str(result.get('main').get('humidity','nn'))
        self.pressure = str(result.get('main').get('pressure','nn'))
        self.image_source = 'http://openweathermap.org/img/w/' + result['weather'][0]['icon'] + '.png'
        self.wind_speed = str(result.get('wind').get('speed','nn'))
        self.wind_direction = str(result.get('wind').get('deg','nn'))
        self.last_update = str(gmtime(result.get('dt')))

        self.notification = ''

    
    def show_forecast(self, request, result):
        '''update displayed data for 5 day forecast.

        The data is stored as described in the OpenWeatherMap API.
        https://openweathermap.org/api/one-call-api?gclid=EAIaIQobChMI1bGR2-Dd6AIVxuN3Ch1sWAgGEAAYAiAAEgK6E_D_BwE

        Args:
            *args (): not used. For further development.
            **kwargs (): not used. For further development.

        Returns:
            (float): Scaled value.

        Raises:
            FileNotFoundError: Raised if forecast.json cannot be found
        '''
                
        self.forecast = result

        #first remove previous forecast 
        self.ids['grid'].clear_widgets()
        
        #add latest info
        for count in self.forecast['list']:

            #the time is formatted using strftime to display only the days name and hh:mm 
            self.ids['grid'].add_widget(Label(text=strftime('%a %H:%M',gmtime(count['dt'])), font_size='30sp'))
            #temperature will be rounded to two decimals
            self.ids['grid'].add_widget(Label(text='{:.0f}'.format(count['main']['temp'] - 273.15) + '°C', font_size='30sp'))
            self.ids['grid'].add_widget(AsyncImage(source='http://openweathermap.org/img/w/' + count['weather'][0]['icon'] + '.png'))

        self.notification = ''

class WeatherTestLayout(BoxLayout):
    pass

class WeatherWidgetApp(App):
    def build(self):
        return WeatherTestLayout()

if __name__ == '__main__':
    WeatherWidgetApp().run()
