import requests
yahoo = 'https://query.yahooapis.com/v1/public/yql?format=json&q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places%20where%20text%3D%22(52.06839%2C5.10569)%22%20limit%201)%20and%20u%3D%22c%22'

class TheWeatherMan:
	def getTodaysWeather():
		resp = requests.get(yahoo)
		if resp.status_code != 200:
		    # This means something went wrong.
		    print('stuk')
		return resp.json()['query']['results']['channel']['item']['condition']