
# Welding Control system
#
# Copyright (C) 2024  Dmitrij Viskunov <viskunovdmitrij1@gmail.com>

import logging
import threading
import serial.tools.list_ports
import serial

# class Connection(object):
    # ToGetData = ""
    # ToSendData = ""
    # AvaliablePorts = []
    # Baudrate = 9600
    # __Device = serial.Serial()
    # def Avaliable(self):
    #     try:
    #         return self.__Device.in_waiting
    #     except Exception as e:
    #         return 0
    # def CheckOut(self):
    #     self.AvaliablePorts.clear()
    #     for port in serial.tools.list_ports.comports():
    #             if port.pid != None:
    #                 self.AvaliablePorts.append((port.name, port.description))
    # def ConnectTo(self, Port:str):
    #     if(len(self.AvaliablePorts) == 0):
    #         return 0
    #     try:
    #         if(self.__Device.is_open):
    #             self.__Device.close()
    #         self.__Device.baudrate = self.Baudrate
    #         self.__Device.port = Port
    #         self.__Device.open()
    #     except Exception as e:
    #         return 0
    #     return 1
    # def Disconnect(self):
    #     try:
    #         self.__Device.close()
    #     except Exception as e:
    #         return 0
    #     return 1
    # def GetData(self):
    #     try:
    #         if(self.__Device.in_waiting):
    #             self.ToGetData = (self.__Device.read_all().decode('utf-8').rstrip())
    #     except Exception as e:
    #         return 0
    #     return 1
    # def SendData(self):
    #     try:
    #         self.ToSendData = str(self.ToSendData)
    #         self.__Device.write(self.ToSendData.encode())
    #     except Exception as e:
    #         return 0
    #     return 1

REPORT_TIME = 1.0


class KnobSlave:
    def __init__(self, config):
        # self.Serial = Connection()
        # self.Serial.Baudrate = 115200
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
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
        # self.Serial.CheckOut()
        # if not self.Serial.AvaliablePorts:
        #     return
        # logging.info(f'Connection: {self.Serial.ConnectTo(self.Serial.AvaliablePorts[0][0])}')
        # while True:
        #     if self.Serial.GetData():
        #         logging.info(f'GET: {self.Serial.ToGetData}')
        #     else:
        #         break
        self.not_working = True
    
    def poll_serial(self, eventtime):
        if self.not_working:
            thread = threading.Thread(target=self.update)
            thread.start()

        measured_time = self.reactor.monotonic()
        return measured_time + REPORT_TIME






def load_config(config):
    return KnobSlave(config)
