import serial.tools.list_ports
import serial
class Connection(object):
    ToGetData = ""
    ToSendData = ""
    AvaliablePorts = []
    Baudrate = 9600
    __Device = serial.Serial()
    def Avaliable(self):
        try:
            return self.__Device.in_waiting
        except Exception as e:
            return 0
    def CheckOut(self):
        self.AvaliablePorts.clear()
        for port in serial.tools.list_ports.comports():
                if port.pid != None:
                    self.AvaliablePorts.append((port.name, port.description))
    def ConnectTo(self, Port:str):
        if(len(self.AvaliablePorts) == 0):
            return 0
        try:
            if(self.__Device.is_open):
                self.__Device.close()
            self.__Device.baudrate = self.Baudrate
            self.__Device.port = Port
            self.__Device.open()
        except Exception as e:
            return 0
        return 1
    def Disconnect(self):
        try:
            self.__Device.close()
        except Exception as e:
            return 0
        return 1
    def GetData(self):
        try:
            if(self.__Device.in_waiting):
                self.ToGetData = (self.__Device.read_all().decode('utf-8').rstrip())
        except Exception as e:
            return 0
        return 1
    def SendData(self):
        try:
            self.ToSendData = str(self.ToSendData)
            self.__Device.write(self.ToSendData.encode())
        except Exception as e:
            return 0
        return 1