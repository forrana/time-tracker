import usocket as socket
import uasyncio as asyncio
import uselect as select
import gc
import json
import re
from index_html import html
from global_vars import manager

def set_color(hex_color):
    manager.led_color = hex_color

def set_background_color(hex_color):
    manager.background_color = hex_color

def set_program(program_id):
    manager.program_number = int(program_id)

def set_delay(delay):
    manager.delay = int(delay)

def set_led_amount(led_amount):
    manager.led_amount = int(led_amount)

def set_led_bits(led_bits):
    manager.led_bits = int(led_bits)

def set_delta_time(delta_time):
    manager.delta_time = int(delta_time)

switcher={
        'program':set_program,
        'color':set_color,
        'delay':set_delay,
        'background_color':set_background_color,
        'led_amount': set_led_amount,
        'led_bits': set_led_bits,
        'delta_time': set_delta_time,
    }

def set_value(key, value):
    value_setter = switcher.get(key, lambda :'Not implemented')
    value_setter(value)

class Server:
    async def run(self, loop):
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        self.socks = [s]

        print('listening on', addr)

        poller = select.poll()
        poller.register(s, select.POLLIN)
        while True:
            res = poller.poll(1)  # 1ms block
            if res:  # Only s_sock is polled
                cl, addr = s.accept()
                loop.create_task(self.run_client(cl, addr, poller))
            await asyncio.sleep_ms(200)
            gc.collect()

    async def run_client(self, sock, cid, poller):
        self.socks.append(sock)
        sreader = asyncio.StreamReader(sock)
        swriter = asyncio.StreamWriter(sock, {})
        print('Got connection from client', cid)
        try:
            is_get_request = True
            content_length = 0
            print('Received from client {}'.format(cid))
            while True:
                res = await sreader.readline()
                if res == b'':
                    raise OSError
                print('{}'.format(res))
                if 'POST' in res:
                    is_get_request = False
                if 'Content-Length' in res:
                    utf8Res = res.decode('UTF-8')
                    content_length = int(utf8Res.split(':')[1])
                if not res or res == b'\r\n':
                    if not is_get_request:
                        res_body = await sreader.read(content_length)
                        body_dict = json.loads(res_body)
                        for key in body_dict.keys():
                            set_value(key, body_dict.get(key))
                    break
            response = ""
            if is_get_request:
                hex_color = manager.led_color_hex
                hex_bg_color = manager.background_color_hex
                led_amount = manager.led_amount
                led_bits = manager.led_bits
                isxchecked = ['']*6
                isxchecked[manager.program_number - 1] = 'checked'
                response = html.format(\
                    color=hex_color, \
                    is1checked=isxchecked[0], \
                    is2checked=isxchecked[1], \
                    is3checked=isxchecked[2], \
                    is4checked=isxchecked[3], \
                    is5checked=isxchecked[4], \
                    is6checked=isxchecked[5], \
                    delay=manager.delay, \
                    background_color=hex_bg_color, \
                    led_amount = led_amount, \
                    led_bits = led_bits, \
                    delta_time = manager.delta_time \
                    )
            else:
                response = "HTTP/1.1 204 No Content\n\r\n"
            await swriter.awrite(response)
            print('Client {} disconnect.'.format(cid))
            sock.close()
            self.socks.remove(sock)
            poller.unregister(sock)
        except OSError:
            pass
        gc.collect()
    def close(self):
        print('closing connection')
        if hasattr(self, 'socks'):
            print('Closing {} sockets.'.format(len(self.socks)))
            for sock in self.socks:
                sock.close()
