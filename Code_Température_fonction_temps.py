import pyb
from pyb import Pin
from pyb import LED
import time
import onewire

leds = [pyb.LED(i+1) for i in range(4)]
leds[0].on()

buf = bytearray(9)
buf_1 = bytearray(9)
buf_2 = bytearray(9)
ow = onewire.OneWire(Pin('X1'))
ox = onewire.OneWire(Pin('X2'))
oy = onewire.OneWire(Pin('X3'))
rom = ow.scan()
romi = oy.scan()
roma = ox.scan()

i = 0
delai1 = 1000
delai2 = 600000
Temp_avec = []
Temp_sans = []
Temp_exterieur = []

while i < 147:
    bidon = ow.reset()
    ow.select_rom(rom[0])
    ow.writebyte(0x44)
    time.sleep_ms(delai1)
    bidon_1 = ox.reset()
    ox.select_rom(roma[0])
    ox.writebyte(0x44)
    time.sleep_ms(delai1)
    bidon_2 = oy.reset()
    oy.select_rom(romi[0])
    oy.writebyte(0x44)
    time.sleep_ms(delai1)

    bidon = ow.reset()
    ow.select_rom(rom[0])
    ow.writebyte(0xBE)

    bidon_1 = ox.reset()
    ox.select_rom(roma[0])
    ox.writebyte(0xBE)

    bidon_2 = oy.reset()
    oy.select_rom(romi[0])
    oy.writebyte(0xBE)

    time.sleep_ms(delai1)
    ow.readinto(buf)
    ox.readinto(buf_2)
    oy.readinto(buf_1)
    msb = buf[1]
    lsb = buf[0]
    msb_1 = buf_1[1]
    lsb_1 = buf_1[0]
    msb_2 = buf_2[1]
    lsb_2 = buf_2[0]

    temp = (float((int('00000111', 2) & msb) << 8) + float(lsb)) / 16
    temp_1 = (float((int('00000111', 2) & msb_1) << 8) + float(lsb_1)) / 16
    temp_2 = (float((int('00000111', 2) & msb_2) << 8) + float(lsb_2)) / 16
    Temp_avec.append(temp)
    Temp_sans.append(temp_1)
    Temp_exterieur.append(temp_2)

    i = i + 1
    time.sleep_ms(delai2)
    print(Temp_avec, Temp_sans, Temp_exterieur)

leds[0].off()
leds[2].on()

with open("/sd/mesures.csv", "w") as f:
    f.write("TP\n")
    f.write("temps en seconde;Temperature\n")
    for j in range(len(Tamp)):
        f.write(str(j * (delai2 + 2 * delai1) / 1000) + ";")
        f.write(str(Temp_avec[j]) + ";")
        f.write(str(Temp_sans[j]) + ";")
        f.write(str(Temp_exterieur[j]) + "\n")

f.close()
leds[2].off()
leds[1].on()
