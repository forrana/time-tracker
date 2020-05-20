import uasyncio as asyncio
import neopixel_programs
# import web_interface
import machine

loop = asyncio.get_event_loop()
loop.create_task(neopixel_programs.start())
# server = web_interface.Server()
# loop.create_task(server.run(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Interrupted')  # This mechanism doesn't work on Unix build.
except MemoryError:
    machine.reset()
#finally:
    # server.close()
