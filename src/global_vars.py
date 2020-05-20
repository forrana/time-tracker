import json


class GlobalVars(object):
    def __init__(self, program_number, led_color, background_color, delay, led_amount, led_bits, delta_time):
        self.state = {}
        self.state['program_number'] = program_number
        self.state['led_color'] = led_color
        self.state['background_color'] = background_color
        self.state['delay'] = delay
        self.state['led_amount'] = led_amount
        self.state['led_bits'] = led_bits
        self.state['delta_time'] = delta_time

    def _color_hex_to_tuple(self, color_hex):
        new_color = color_hex.replace("#", "")
        color_array_hex = [new_color[i:i+2] for i in range(0, len(new_color), 2)]
        color_array_hex.append('00')
        color_array_decimal = map(lambda  x:int(x,16), color_array_hex)
        return tuple(color_array_decimal)

    def _color_tuple_to_hex(self, color_tuple):
        return "%0.2X%0.2X%0.2X" % (color_tuple[0], color_tuple[1], color_tuple[2])

    @property
    def delay(self):
        return self.state.get('delay')

    @property
    def delta_time(self):
        return self.state.get('delta_time')

    @property
    def led_amount(self):
        return self.state.get('led_amount')

    @property
    def led_bits(self):
        return self.state.get('led_bits')

    @property
    def program_number(self):
        return self.state.get('program_number')

    @property
    def led_color(self):
        return self.state.get('led_color')

    @property
    def led_color_hex(self):
        return self._color_tuple_to_hex(self.state['led_color'])

    @property
    def background_color(self):
        return self.state.get('background_color')

    @property
    def background_color_hex(self):
        return self._color_tuple_to_hex(self.state['background_color'])

    @led_color.setter
    def led_color(self, value):
        if isinstance(value, tuple):
            self.state['led_color'] = value
        elif isinstance(value, str):
            self.state['led_color'] = self._color_hex_to_tuple(value)
        self.save_state()

    @background_color.setter
    def background_color(self, value):
        if isinstance(value, tuple):
            self.state['background_color'] = value
        elif isinstance(value, str):
            self.state['background_color'] = self._color_hex_to_tuple(value)
        self.save_state()

    @program_number.setter
    def program_number(self, value):
        self.state['program_number'] = value
        self.save_state()

    @delay.setter
    def delay(self, value):
        self.state['delay'] = value
        self.save_state()

    @led_amount.setter
    def led_amount(self, value):
        self.state['led_amount'] = value
        self.save_state()

    @delta_time.setter
    def delta_time(self, value):
        self.state['delta_time'] = value
        self.save_state()

    @led_bits.setter
    def led_bits(self, value):
        self.state['led_bits'] = value
        self.save_state()

    def save_state(self):
        f = open('state.txt', 'w')
        f.write(json.dumps(self.state))
        f.close()

    def load_state(self):
        f = None
        try:
            f = open('state.txt')
            state_string = f.readline()
            if state_string:
                self.state = json.loads(state_string)
        except:
            print('File does not exist')
            pass
        finally:
            if f:
                f.close()


manager = GlobalVars(1, (166, 16, 30), (0, 0, 0), 100, 5, 3, 3)
manager.load_state()
