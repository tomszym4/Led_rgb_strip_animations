import utime
from neopixel import Neopixel
import uasyncio
from gpio_lcd import GpioLcd
from machine import Pin, PWM

lcd = GpioLcd(rs_pin=Pin(18), enable_pin=Pin(17), d4_pin=Pin(20), d5_pin=Pin(19),
              d6_pin=Pin(22), d7_pin=Pin(21), num_lines=2, num_columns=16)

lcd_freq = PWM(Pin(16))
lcd_freq.duty_u16(26000)
button1 = Pin(0, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(4, Pin.IN, Pin.PULL_DOWN)
button_stop = Pin(5, Pin.IN, Pin.PULL_DOWN)

numpix = 120
strip = Neopixel(numpix, 0, 9, "GRB")

red = (255, 0, 0)
green = (0, 255, 0)
teal = (64, 218, 255)
blue = (0, 0, 255)
orange = (255, 165, 0)
yellow = (255, 150, 0)
indigo = (75, 0, 130)
violet = (138, 43, 226)
purple = (212, 40, 255)
colors_rgb = (red, orange, yellow, green, teal, blue, indigo, violet, purple)
colors = colors_rgb


def check_stop_button():
    if button_stop.value() == 1:
        return True
    else:
        return False


def change_color(pixel, color):
    strip.set_pixel(pixel, colors_rgb[color])


def rainbow(x):
    lcd.move_to(0, 1)
    lcd.putstr("           stop>")
    step = round(numpix / len(colors))
    current_pixel = 0
    strip.brightness(x)
    strip.show()
    for color1, color2 in zip(colors, colors[1:]):
        strip.set_pixel_line_gradient(current_pixel, current_pixel + step, color1, color2)
        current_pixel += step
    strip.set_pixel_line_gradient(current_pixel, numpix - 1, violet, red)

    while True:
        strip.rotate_right(1)
        strip.show()
        utime.sleep(0.042)
        if check_stop_button():
            strip.clear()
            strip.show()
            return 1


def check_gradient():
    count = 20
    current_pixel = 0
    color1 = violet
    color2 = blue
    strip.set_pixel_line_gradient(current_pixel, current_pixel + count - 1, color2, color1)
    strip.show()
    while True:
        if check_stop_button():
            strip.clear()
            strip.show()
            return


def flowing_two_colors(x):
    lcd.move_to(0, 1)
    lcd.putstr("           stop>")
    current_pixel = 0
    length = 10
    strip.brightness(x)
    strip.show()
    for j in range(6):
        strip.set_pixel_line(current_pixel, current_pixel + length, teal)
        strip.set_pixel_line(current_pixel + length, current_pixel + (2 * length), purple)
        current_pixel += 2 * length

    while True:
        strip.rotate_right(1)
        strip.show()
        utime.sleep(0.07)
        if check_stop_button():
            strip.clear()
            strip.show()
            return 1


def breathing_all_colors(x):
    lcd.move_to(0, 1)
    lcd.putstr("           stop>")
    current_pixel = 0
    level = 0
    max_brightness = 150
    ascending = True
    strip.brightness(x)
    strip.show()
    num_color = 0
    while True:
        if ascending:
            strip.brightness(level)
            strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
            strip.show()
            level += 1
            if level >= max_brightness:
                ascending = False
        elif not ascending:
            strip.brightness(level)
            strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
            strip.show()
            level -= 1
            if level <= 0:
                ascending = True
        if level == 0:
            num_color += 1
            if num_color >= len(colors_rgb) - 1:
                num_color = 0
            change_color(current_pixel, num_color)
        if check_stop_button():
            for x in range(level, 0, -1):
                strip.brightness(x)
                strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
                strip.show()
                utime.sleep(0.0005)
            strip.clear()
            strip.show()
            return 1
        utime.sleep(1/max_brightness)


def breathing_oce_color(x):
    lcd.move_to(0, 1)
    lcd.putstr("    color  stop>")
    current_pixel = 0
    level = 0
    max_brightness = 150
    ascending = True
    strip.brightness(x)
    strip.show()
    num_color = 0
    button2_pushed = False
    while True:
        if ascending:
            strip.brightness(level)
            strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
            strip.show()
            level += 1
            if level >= max_brightness:
                ascending = False
        elif not ascending:
            strip.brightness(level)
            strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
            strip.show()
            level -= 1
            if level <= 1:
                ascending = True
        if button2.value() == 1 and not button2_pushed:
            button2_pushed = True
            num_color += 1
            if num_color >= len(colors_rgb) - 1:
                num_color = 0
            change_color(current_pixel, num_color)
        elif button2.value() == 0 and button2_pushed:
            button2_pushed = False
        if check_stop_button():
            for x in range(level, 0, -1):
                strip.brightness(x)
                strip.set_pixel_line(current_pixel, numpix - 1, colors_rgb[num_color])
                strip.show()
                utime.sleep(0.0005)
            strip.clear()
            strip.show()
            return 1
        utime.sleep(1/max_brightness)


def shadow(x):
    lcd.move_to(0, 1)
    lcd.putstr("    color  stop>")
    count = 10
    current_pixel = 0
    color2 = (0, 0, 0)
    num_color = 0
    strip.set_pixel_line_gradient(current_pixel, current_pixel - count, color2, colors_rgb[num_color])
    strip.brightness(x)
    strip.show()
    button2_pushed = False
    while True:
        current_pixel += 1
        if current_pixel > numpix - 1:
            current_pixel = 0
        strip.rotate_right(1)
        strip.show()
        utime.sleep(0.03)
        if button2.value() == 1 and not button2_pushed:
            button2_pushed = True
            num_color += 1
            if num_color > len(colors_rgb) - 1:
                num_color = 0
            strip.set_pixel_line_gradient(current_pixel, current_pixel - count, color2, colors_rgb[num_color])
        elif button2.value() == 0 and button2_pushed:
            button2_pushed = False
        if check_stop_button():
            strip.clear()
            strip.show()
            return 1


def ping_pong(x):
    lcd.move_to(0, 1)
    lcd.putstr("    color  stop>")
    current_pixel = 0
    num_color = 0
    strip.set_pixel(current_pixel, colors_rgb[num_color])
    strip.brightness(x)
    strip.show()
    ascending = True
    button2_pushed = False
    while True:
        if ascending:
            strip.rotate_right(1)
            strip.show()
            utime.sleep(0.03)
            current_pixel += 1
            if current_pixel > numpix - 1:
                ascending = False
        elif not ascending:
            strip.rotate_left(1)
            strip.show()
            utime.sleep(0.03)
            current_pixel -= 1
            if current_pixel < 1:
                ascending = True
        if button2.value() == 1 and not button2_pushed:
            button2_pushed = True
            num_color += 1
            if num_color >= len(colors_rgb) - 1:
                num_color = 0
            change_color(current_pixel, num_color)
        elif button2.value() == 0 and button2_pushed:
            button2_pushed = False
        if check_stop_button():
            strip.clear()
            strip.show()
            return 1


def print_name(x):
    lcd.clear()
    lcd.move_to(0, 0)
    lcd.putstr(x)


def print_menu():
    lcd.move_to(0, 1)
    lcd.putstr("<back  GO  next>")


async def main():
    current_program = 0
    button1_pushed = False
    button2_pushed = False
    button_stop_pushed = False
    current_brightness = 255
    strip.brightness(current_brightness)
    all_programs = [lambda: rainbow(current_brightness), lambda: ping_pong(current_brightness),
                    lambda: shadow(current_brightness), lambda: breathing_oce_color(current_brightness),
                    lambda: breathing_all_colors(current_brightness), lambda: flowing_two_colors(current_brightness)]
    programs = ["Rainbow", "Ping Pong", "Shadow", "Tide", "Breathing", "Flow"]
    print_name(programs[current_program])
    print_menu()
    while True:
        if button1.value() == 1 and not button1_pushed:
            button1_pushed = True
            current_program -= 1
            if current_program < 0:
                current_program = len(all_programs) - 1
            print_name(programs[current_program])
            print_menu()
        elif button1.value() == 0 and button1_pushed:
            button1_pushed = False
        if button_stop.value() == 1 and not button_stop_pushed:
            button_stop_pushed = True
            current_program += 1
            if current_program >= len(all_programs):
                current_program = 0
            print_name(programs[current_program])
            print_menu()
        elif button_stop.value() == 0 and button_stop_pushed:
            button_stop_pushed = False
        if button2.value() == 1 and not button2_pushed:
            button2_pushed = True
            if all_programs[current_program]() == 1:
                current_program -= 1
                print_menu()

        elif button2.value() == 0 and button2_pushed:
            button2_pushed = False
        utime.sleep(0.04)


uasyncio.run(main())
