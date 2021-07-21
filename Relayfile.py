from Settings import *


class Relays:
    def __init__(self, rid, name, ip, relay_number, start_time, end_time, status="OFF"):
        self.rid = rid
        self.name = name
        self.ip = ip
        self.relay_number = relay_number
        self.start_time = start_time
        self.end_time = end_time
        self.__status = status
        self.button = None
        self.edit_btn = None
        self.delete_btn = None

    def Relay_ON(self):
        send(self.ip, f"RELAY{self.relay_number}:ON")
        self.__status = "ON"

    def Relay_OFF(self):
        send(self.ip, f"RELAY{self.relay_number}:OFF")
        self.__status = "OFF"

    def get_status(self):
        return self.__status


def send(ip, data):
    print(f"I`m sanding Data<{data}> to IP<{ip}>")


# object_name = input("Choose relay name to update>>>")
if __name__ == "__main__":
    my_relays = []  # esi mer datark listn a, vori mej piti linen mer releneri obyektnery
    my_file = Read_file("Config.txt")
    info = my_file.get_relay_info()
    for relay in info:
        r = Relays(relay["Name"], relay["IP"], relay["Relay"], relay["start"], relay["end"], relay["status"])
        my_relays.append(r)
    new = {
        "Name": input("Name>"),
        "IP": input("IP>"),
        "Relay": input("Relay in IP>"),
        "start": input("start time>"),
        "end": input("end time>")
    }

    my_file.add_relay_info(new["Name"], new["IP"], new["Relay"], new["start"], new["end"])
