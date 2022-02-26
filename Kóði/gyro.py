import smbus, math, time, os, requests
from datetime import datetime

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    return bus.read_byte_data(address, reg)

def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def getWeatherApi(city = "Keflavik", key = "ec287ad7a92b087d609e988f0b9dee8a"):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + key + "&q=" + city
    request = requests.get(complete_url)
    return request.json()

def getTemp(json):
    weather = json['main']
    current_temperature = weather["temp"]
    return round(current_temperature-273.15)

def getWeather(json):
    weather = json["weather"]
    weather_description = weather[0]["description"]
    return str(weather_description)

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

counter = 10
timer = 60

bus.write_byte_data(address, power_mgmt_1, 0)
while True:
  X_out = read_word_2c(0x3b) / 16384.0
  Y_out = read_word_2c(0x3d) / 16384.0
  Z_out = read_word_2c(0x3f) / 16384.0

  X = get_x_rotation(X_out, Y_out, Z_out)
  Y = get_y_rotation(X_out, Y_out, Z_out)

  os.system('clear')

  if counter == 10:
        response = getWeatherApi()
        counter = 0
  counter += 1

  kl = datetime.now()

  if abs(X)<=40 and Y<0:
    #UP
    timer = 60
    print(kl.strftime("%H:%M:%S"))
  elif abs(X)<=40 and Y>0:
    #DOWN
    timer = 60
    print("down")
  elif X>40:
    #LEFT
    timer = 60
    print(getWeather(response),str(getTemp(response))+"°C")
  elif X<-40:
    #RIGHT
    print("01:00" if timer == 60 else "Time's up" if timer <= 0 else "00:"+str(timer/10)[::2])
    timer -= 1
  time.sleep(1)