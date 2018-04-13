from datetime import datetime
from datetime import timedelta
import urllib3
import json

class CO2Fetcher(object):

    def __init__(self):
        self._http = urllib3.PoolManager()
        self._url = 'http://api.energidataservice.dk/datastore_search?resource_id=b5a8e0bc-44af-49d7-bb57-8f968f96932d&limit=5&filters={%22PriceArea%22:%20%22DK2%22}&q='

    def _calcLookuptime(self, timestamp):
        timestamp = timestamp - timedelta(0,0,0,0,timestamp.minute % 5)
        timestamp = timestamp - timedelta(0,0,0,0,10)
        return timestamp

    def _formatLookuptime(self, timestamp):
        timestring = "%i-%02i-%02iT%02i:%02i" % (timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute)
        return timestring

    def _GetCO2Data(self, timestring):
        completeUrl = self._url + timestring
        r = self._http.request('GET', completeUrl)
        #print (r.data)
        d=json.loads(r.data.decode('utf-8'))
        d=d['result']
        d=d['records']
        d=d[0]
        d=d['CO2Emission']
        #print(d)
        return d

    def getCO2Avgr(self, minutes, timestamp):
        loopCount = 0;
        co2 = 0;
        try:
            timestamp = self._calcLookuptime(timestamp)
            while (0<minutes):
                timestr = self._formatLookuptime(timestamp)
                co2 = co2 + self._GetCO2Data(timestr)
                minutes = minutes - 15
                timestamp = timestamp - timedelta(0, 0, 0, 0, 15)
                loopCount = loopCount +1 
                #print(timestr)
                #print(co2)
            co2avg = co2/loopCount
        except:
            co2avg = ' '
        #print(co2avg)
        return co2avg

"""
#test code
fetch = CO2Fetcher()
now = datetime.now()
fetch.getCO2Avgr(60, now)
"""
