import datetime, calendar

datetimeformat = "%Y-%m-%d %H:%M:%S"

# ubxtool  -t -p NAV-TIMELS -P 29.20
# UBX-NAV-TIMELS:
#  iTOW 144529000 version 0 reserved2 0 0 0 srcOfCurrLs 2
#  currLs 18 srcOfLsChange 2 lsChange 0 timeToLsEvent -66672511
#  dateOfLsGpsWn 2185 dateOfLsGpsDn 7 reserved2 0 0 0
#  valid x3

# after reading from ubxtool dateOfLsGpsWn
gpsWn=2290

# after reading from ubxtool dateOfLsGpsDn
gpsDn=7

epoch = datetime.datetime.strptime("1980-01-06 00:00:00",datetimeformat)
elapsed = datetime.timedelta(days=(gpsWn*7), seconds=(gpsDn*86400))

# absolute time
print("GPS absolute time: ", datetime.datetime.strftime(epoch+elapsed, datetimeformat))
# timestamp
print("GPS timestamp: ", datetime.datetime.timestamp(epoch+elapsed))