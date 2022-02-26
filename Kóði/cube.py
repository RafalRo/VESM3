from samplebase import SampleBase
from rgbmatrix import graphics
from datetime import datetime
import time, requests

def getWeatherApi(city = "Keflavik", key = "ec287ad7a92b087d609e988f0b9dee8a"):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + key + "&q=" + city
    request = requests.get(complete_url)
    return request.json()

def getTemp(jsn):
    weather = jsn['main']
    current_temperature = weather["temp"]
    return int(current_temperature-273.15)
    
class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        
        def run(self):
            offscreen_canvas = self.matrix.CreateFrameCanvas()
            font = graphics.Font()
            font.LoadFont("../../../fonts/10x20.bdf")
            textColor = graphics.Color(64, 96, 128)
            counter = 800
            while True:
                kl = datetime.now()
                kl = kl.strftime("%H:%M")
                offscreen_canvas.Clear()
                if counter == 800:
                    response = getWeatherApi()
                    counter = 0
                    temp = str(getTemp(response))+"°C"
                    len = graphics.DrawText(offscreen_canvas, font, 7, 21, textColor, kl)
                    len = graphics.DrawText(offscreen_canvas, font, 17, 53, textColor, temp)
                    time.sleep(0.05)
                    counter += 1
                    offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                    
# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()