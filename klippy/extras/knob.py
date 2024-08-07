
# Welding Control system
#
# Copyright (C) 2024  Dmitrij Viskunov <viskunovdmitrij1@gmail.com>

import logging
import socket
import threading
REPORT_TIME = 1.0


class KnobSlave:
    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.i = 0
        self.gcode_move = self.printer.lookup_object("gcode_move")
        self.gcode = self.printer.lookup_object("gcode")
        self.server = self.printer.lookup_object("webhooks")
        self.sample_timer = self.reactor.register_timer(self.poll_serial)
        self.server.register_endpoint("knob/change_param", self.change_param)
        self.printer.register_event_handler('klippy:connect', self.handle_connect)
        self.not_working = True

    def handle_connect(self):
        self.reactor.update_timer(self.sample_timer, self.reactor.NOW)

    def change_param(self, webrequest):
        name = webrequest.get_str('name')
        value = webrequest.get_str('value')
        if name == "extruder_speed":
            self.gcode.run_script_from_command(f'M220 S{value}')
    def get_status(self, eventtime):
        return {'extruder_speed': self.gcode_move.extrude_factor * 100}
    
    def update(self):
        self.not_working = False
        self.i += 1
        logging.info(f'CUR: {self.i}')
        print(f'CUR: {self.i}')
        self.not_working = True
    
    def poll_serial(self, eventtime):
        if self.not_working:
            thread = threading.Thread(target=self.update)
            thread.start()

        measured_time = self.reactor.monotonic()
        return measured_time + REPORT_TIME






def load_config(config):
    return KnobSlave(config)
