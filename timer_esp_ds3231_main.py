# ESP32 DS3231 / AT24C32 MicroPython Code Example
# integrates DS3231 / AT24C32 Real-Time Clock (RTC) with ESP32
# https://www.espboards.dev/sensors/ds3231/#ds3231-espidf

from machine import I2C, Pin
import time

# DS3231 I2C address
DS3231_ADDRESS = 0x68

def bcd_to_decimal(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

def decimal_to_bcd(decimal):
    return ((decimal // 10) << 4) | (decimal % 10)

def set_time(i2c, year, month, day, hour, minute, second):
    data = [decimal_to_bcd(second), decimal_to_bcd(minute), decimal_to_bcd(hour),
            decimal_to_bcd(day), 0, decimal_to_bcd(month), decimal_to_bcd(year - 2000)]
    i2c.writeto_mem(DS3231_ADDRESS, 0x00, bytes(data))

def get_time(i2c):
    data = i2c.readfrom_mem(DS3231_ADDRESS, 0x00, 7)
    second = bcd_to_decimal(data[0])
    minute = bcd_to_decimal(data[1])
    hour = bcd_to_decimal(data[2])
    day = bcd_to_decimal(data[4])
    month = bcd_to_decimal(data[5] & 0x1F)
    year = bcd_to_decimal(data[6]) + 2000
    return year, month, day, hour, minute, second

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Set initial time
set_time(i2c, 2023, 12, 4, 14, 30, 0)

# Loop to read time
while True:
    year, month, day, hour, minute, second = get_time(i2c)
    print(f"Time: {hour:02}:{minute:02}:{second:02}, Date: {year:04}/{month:02}/{day:02}")
    time.sleep(1)
