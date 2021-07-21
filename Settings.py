class Read_file:
    def __init__(self, file):
        self.file = file

    def add_relay_info(self, name, IP, Relay, start, end):
        with open(self.file, "a") as config_file:
            text = name + "%" + IP + "%" + Relay + "%" + start + "%" + end + "%OFF\n"
            config_file.write(text)

    def get_relay_info(self):
        with open(self.file, "r") as config_file:
            text = config_file.readlines()
            relays = []
            for each_line in text:
                l = {}
                line = each_line.split('%')
                l["Name"] = line[0]
                l["IP"] = line[1]
                l["Relay"] = line[2]
                l["start"] = line[3]
                l["end"] = line[4]
                l["status"] = line[5][:-1]
                relays.append(l)
        return relays

    def update_relay_info(self, name, new_list):
        relay_list = self.get_relay_info()
        with open(self.file, "w") as config_file:
            for relay in relay_list:
                if relay["Name"] == name:
                    text = new_list["Name"] + "%" + \
                           new_list["IP"] + "%" + \
                           new_list["Relay"] + "%" + \
                           new_list["start"] + "%" + \
                           new_list["end"] + "%OFF\n"
                else:
                    text = relay["Name"] + "%" + \
                           relay["IP"] + "%" + \
                           relay["Relay"] + "%" + \
                           relay["start"] + "%" + \
                           relay["end"] + "%OFF\n"
                config_file.write(text)

    def delete_relay_info(self, name):
        relay_list = self.get_relay_info()
        with open(self.file, "w") as config_file:
            for relay in relay_list:
                if relay["Name"] == name:
                    continue
                else:
                    text = relay["Name"] + "%" + relay["IP"] + "%" + relay["Relay"] + "%" + \
                           relay["start"] + "%" + relay["end"] + "%OFF\n"
                config_file.write(text)
