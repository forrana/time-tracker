# This is script that run when device boot up or wake from sleep.
import uasyncio as asyncio
import machine, neopixel
from machine import TouchPad, Pin
import gc
from global_vars import manager
import urandom
from utime import time

np = neopixel.NeoPixel(machine.Pin(2), manager.led_amount, bpp=manager.led_bits)
buzzer = Pin(27, Pin.OUT)

button = TouchPad(Pin(4))
button.config(500)

led_bits = manager.led_bits
MAX_BRIGHTNESS = 255


async def wait_pin_change(pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 500ms
    active = 0
    while active < 100:
        if button.read() < 400:
            active += 1
        else:
            active = 0
        await asyncio.sleep_ms(1)

async def wait_pin_to_untap(pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 500ms
    active = 0
    buzzer.value(1)
    while active < 20:
        if button.read() > 700:
            active += 1
        else:
            active = 0
        await asyncio.sleep_ms(1)
    buzzer.value(0)


def get_n_bits_color_tuple(red, green, blue, white, n):
    if(n == 3):
        return (red, green, blue)
    elif(n == 4):
        return (red, green, blue, white)

async def clear(np, delay, color, background_color, subprogram):
    n = np.n
    for i in range(n):
        np[i] = get_n_bits_color_tuple(0,0,0,0,led_bits)
    np.write()
    # await asyncio.sleep_ms(1)

async def sleep_for_n_ms(delay_ms):
    for i in range(delay_ms/10):
        await asyncio.sleep_ms(10)
        if button.read() < 400:
            active += 1
        else:
            active = 0
        if active > 10:
            active = 0
            await wait_pin_to_untap(button)
            return True
    return False



async def render(n, start_red, start_green, start_blue, delay_ms):
    for i in range(np.n):
            np[i] = get_n_bits_color_tuple(0, 0, 0, 0,led_bits)
    for i in range(n):
        np[i] = get_n_bits_color_tuple(255, 255, 255, 0,led_bits)
    np[n] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
    np.write()

    paused = 0
    for i in range(int(delay_ms/10)):
        await asyncio.sleep_ms(10)
        if button.read() < 400:
            paused += 1
        else:
            paused = 0

        if paused > 5:
            is_paused = True
            paused = 0
            active = 0
            await wait_pin_to_untap(button)
            while is_paused:
                np[n] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
                np.write()
                is_paused = sleep_for_n_ms(500)
                np[n] = get_n_bits_color_tuple(0, 0, 0, 0,led_bits)
                np.write()
                is_paused = sleep_for_n_ms(500)
                np[n] = get_n_bits_color_tuple(start_red, start_green, start_blue,0,led_bits)
                np.write()

async def count_N_minutes(np, minutes, reverse = False):
    delay_ms = int(200*(minutes/5))
    start = 0
    stop = np.n
    step = 1
    color_step = 4
    if reverse:
        start = np.n - 1
        stop = -1
        step = -1
        color_step = -4
    for n in range(start, stop, step):
        start_red = 0
        start_green = 0
        start_blue = 0
        for color_counter in range(60):
            start_red += color_step
            await render(n, start_red, start_green, start_blue, delay_ms)
        for color_counter in range(60):
            start_blue += color_step
            await render(n, start_red, start_green, start_blue, delay_ms)
        for color_counter in range(60):
            start_red -= color_step
            start_blue -= color_step
            start_green += color_step
            await render(n, start_red, start_green, start_blue, delay_ms)
        for color_counter in range(60):
            start_green -= color_step
            start_blue += color_step
            await render(n, start_red, start_green, start_blue, delay_ms)
        for color_counter in range(60):
            start_green += color_step
            start_red += color_step
            await render(n, start_red, start_green, start_blue, delay_ms)

async def blinkingMode(n):
    restartProgram = False
    while restartProgram == False:
        for i in range(np.n):
            np[i] = get_n_bits_color_tuple(255, 255, 255, 0,led_bits)
        np.write()
        if sleep_for_n_ms(500):
            return
        buzzer.value(1)
        for i in range(np.n):
            np[i] = get_n_bits_color_tuple(0, 0, 0, 0,led_bits)
        np.write()
        if sleep_for_n_ms(200):
            return
        buzzer.value(0)
        if sleep_for_n_ms(300):
            return

async def start_program(np, delay, color, background_color, subprogram):
    await count_N_minutes(np, 25)
    await blinkingMode(np)
    await count_N_minutes(np, 5, True)
    await blinkingMode(np)

async def indirect(programm, subprogram=0):
    switcher={
            0:clear,
            1:start_program,
            }
    func=switcher.get(programm, lambda :'Invalid')
    return await func(np, manager.delay, manager.led_color, manager.background_color, subprogram)

async def start():
    await indirect(0)
    await wait_pin_change(button)
    print("neopixel start")
    start = time()
    while True:
        await wait_pin_to_untap(button)
        await indirect(1)
