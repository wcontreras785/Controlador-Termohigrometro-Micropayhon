from machine import SoftI2C, Pin, RTC
import onewire, ds18x20, time
import utime, dht, network, urequests
import OLED, ntptime
from utelegram import Bot

TOKEN = '5140355036:AAHV6ctlDC61689ehmPeqH0vADdayHgWDks'
temp=37
bot = Bot(TOKEN)
ntptime.settime()
#------------------------------------------WIFI-------------------
def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              #Si no está conectado…
          miRed.active(True)                   #activa la interface
          miRed.connect(red, password)         #Intenta conectar con la red
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():           #Mientras no se conecte..
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True
if conectaWifi (".", "V5MVH6F3SVDU"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
#------------------------------------------WIFI-------------------
#-------------------------------------------Telegram-----------
    @bot.add_message_handler('hola')
    def help(update):
        update.reply('Escribir on/off')
#-------------------------------------------Telegram-----------
#--------------------------SINCRONIZACIÓN DEL RELOJ INTERNO E IMPRESIÓN DE FECHA Y HORA----------------------
rtc= RTC()
(year, month, mday, weekday, hour, minute, second, milisecond)=rtc.datetime()                
rtc.init((year, month, mday, weekday, hour-5, minute, second, milisecond))   # GMT corrección -Colombia-: GMT-5 

def rfecha(): 
    print ("Fecha: {:02d}/{:02d}/{}".format(rtc.datetime()[2],
                                        rtc.datetime()[1],
                                        rtc.datetime()[0]))
def rhora():
    print ("Hora: {:02d}:{:02d}:{:02d}".format(rtc.datetime()[4],
                                           rtc.datetime()[5],
                                           rtc.datetime()[6]))
rfecha()
rhora()
#print (rtc.datetime())
#---------------------------------Oled------
i2c = SoftI2C(scl=Pin(4), sda=Pin(16)) # pines I2C
oled = OLED.SSD1306_I2C(128,64,i2c)
#-----------------------------------DHT-------
pindht =Pin(15, Pin.IN)
dht11 = dht.DHT11(pindht)
#-----------------------------------DS18B20----------
ds_pin=Pin(5)
ds = ds18x20.DS18X20(onewire.OneWire(ds_pin)) 
roms = ds.scan()
#-----------------------------------mocs------------------
moc1=Pin(33, Pin.OUT)
moc2=Pin(32, Pin.OUT)
#-----------------------------------Botones--------------
btn1=Pin(23, Pin.IN, Pin.PULL_UP) # 1 AL OPRIMIR 0
btn2=Pin(22, Pin.IN, Pin.PULL_DOWN)# 0 AL OPRIMIR 1
def ftemp():
    global temp
    print(round(temp,2))
    if btn1.value()==0:
        temp=temp+0.1
    if btn2.value()==1:
        temp=temp-0.1
    utime.sleep_ms(50)
    
def calor():
    if t < temp or t2 < temp:
        moc1.value(1)
        print("calentando")
    else:
        moc1.value(0)
def motor():
    utime.sleep(5)
    moc2.value(1)
    utime.sleep(5)
    moc2.value(0)
while True:
    ftemp()
#-----------------------------------dht11------------
    dht11.measure()
    t=dht11.temperature()
    h=dht11.humidity()
    
#----------------------------------DS18B20----------
    ds.convert_temp()
    utime.sleep_ms(750) #The reading temperature needs at least 750ms
    for rom in roms:
        oled.fill(0)
        t2=ds.read_temp(rom)
        oled.text("T2: "+ str(round(t2,2)),5,30)  

    oled.text("T1: "+ str(t) +" C",5,20)
    oled.text("Hum:"+ str(h) +" %",5,50)
    oled.text("tem:"+ str(round(temp,2)) +" %",5,0)
    oled.show()
