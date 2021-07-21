from tkinter import *
from Relayfile import *
import time

tk = Tk()
new_tk = None
edit = False
T_name = None
T_ip = None
T_rnumber = None
T_start = None
T_end = None
last_name = None
tk_update_dict = {
    "edit": None,
    "Name": None,
    "IP": None,
    "Relay": None,
    "start": None,
    "end": None,
    "lname": None
}
my_relays = []  # esi mer datark listn a, vori mej piti linen mer releneri obyektnery
my_file = Read_file("Config.txt")
info = my_file.get_relay_info()

iterator = 0
for relay in info:
    r = Relays(iterator, relay["Name"], relay["IP"], relay["Relay"], relay["start"], relay["end"], relay["status"])
    my_relays.append(r)
    iterator += 1
app_running = True
new_app_running = True
size_canvas_x = 1000
size_canvas_y = 600


def on_closing():
    global app_running
    if messagebox.askyesno("Выход из программы", "Хотите выйти из программы?"):
        app_running = False
        tk.destroy()


def new_on_closing():
    global new_app_running
    global new_tk
    new_app_running = False
    new_tk.destroy()


tk.protocol("WM_DELETE_WINDOW", on_closing)

tk.title("Light control Server")
tk.resizable(0, 0)
# tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_canvas_x, height=size_canvas_y, bd=0, highlightthickness=0)  # + menu_x
canvas.create_rectangle(0, 0, size_canvas_x, size_canvas_y, fill="grey90")
canvas.pack()
my_menu = Menu(tk)
tk.config(menu=my_menu)
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_command(label="Новый", command=lambda: new_relay())
tk.update()


def button_on_light(args):
    if args.get_status() == "OFF":
        args.Relay_ON()
        args.button.configure(text=args.name + ":" + args.get_status(), bg="yellow")
    elif args.get_status() == "ON":
        args.Relay_OFF()
        args.button.configure(text=args.name + ":" + args.get_status(), bg="grey")
    messagebox.showinfo(args.name, args.get_status())


def new_relay():
    new_window()


def edit_button(param):
    new_window(param)


def new_window(param=None):
    global new_app_running
    global new_tk
    global tk_update_dict
    global edit
    global T_name
    global T_ip
    global T_rnumber
    global T_start
    global T_end
    global last_name

    new_app_running = True
    edit = False
    last_name = ""
    ip = ""
    relay_number = ""
    start_time = ""
    end_time = ""

    if param is not None:
        edit = True
        last_name = param.name
        ip = param.ip
        relay_number = param.relay_number
        start_time = param.start_time
        end_time = param.end_time
    new_tk = Tk()
    new_tk.geometry('300x300')
    new_tk.protocol("WM_DELETE_WINDOW", new_on_closing)
    new_tk.title("Light control Server")
    new_tk.resizable(0, 0)
    # tk.wm_attributes("-topmost", 1)

    l_name = Label(new_tk, text="Name")
    l_name.place(x=10, y=10)
    T_name = Text(new_tk, height=1, width=20)
    T_name.place(x=100, y=10)
    T_name.insert(INSERT, last_name)
    l_ip = Label(new_tk, text="IP")
    l_ip.place(x=10, y=40)
    T_ip = Text(new_tk, height=1, width=20)
    T_ip.place(x=100, y=40)
    T_ip.insert(INSERT, ip)
    l_rnumber = Label(new_tk, text="Relay Number")
    l_rnumber.place(x=10, y=70)
    T_rnumber = Text(new_tk, height=1, width=20)
    T_rnumber.place(x=100, y=70)
    T_rnumber.insert(INSERT, relay_number)
    l_start = Label(new_tk, text="Start Time")
    l_start.place(x=10, y=100)
    T_start = Text(new_tk, height=1, width=20)
    T_start.place(x=100, y=100)
    T_start.insert(INSERT, start_time)
    l_end = Label(new_tk, text="End_time")
    l_end.place(x=10, y=130)
    T_end = Text(new_tk, height=1, width=20)
    T_end.place(x=100, y=130)
    T_end.insert(INSERT, end_time)
    tk_update_dict = {
        "edit": edit,
        "Name": T_name.get("1.0", END)[:-1],
        "IP": T_ip.get("1.0", END)[:-1],
        "Relay": T_rnumber.get("1.0", END)[:-1],
        "start": T_start.get("1.0", END)[:-1],
        "end": T_end.get("1.0", END)[:-1],
        "lname": last_name

    }
    b1 = Button(new_tk, text="Save", width=10, height=2, command=Save_button_click)
    b2 = Button(new_tk, text="Cancel", width=10, height=2, command=new_on_closing)
    b1.place(x=175, y=220)
    b2.place(x=50, y=220)

    new_tk.update()
    while new_app_running:
        if new_app_running:
            new_tk.update_idletasks()
            new_tk.update()
        else:
            new_tk.destroy()
        time.sleep(0.005)
    update_buttons()


def delete_button(rid):
    if messagebox.askyesno("Удалить?", "Хотите удалить данный объект?"):
        my_file.delete_relay_info(my_relays[rid].name)
        update_buttons()


def Save_button_click():
    global new_app_running
    global tk_update_dict
    global edit
    global T_name
    global T_ip
    global T_rnumber
    global T_start
    global T_end
    global last_name
    tk_update_dict = dict(
        edit=edit,
        Name=T_name.get("1.0", END)[:-1],
        IP=T_ip.get("1.0", END)[:-1],
        Relay=T_rnumber.get("1.0", END)[:-1],
        start=T_start.get("1.0", END)[:-1],
        end=T_end.get("1.0", END)[:-1],
        lname=last_name)
    if tk_update_dict["edit"]:
        my_file.update_relay_info(tk_update_dict["lname"], tk_update_dict)
    else:
        my_file.add_relay_info(tk_update_dict["Name"],
                               tk_update_dict["IP"],
                               tk_update_dict["Relay"],
                               tk_update_dict["start"],
                               tk_update_dict["end"])
    new_on_closing()


def update_buttons():
    global tk
    global my_relays
    for each in my_relays:
        each.button.destroy()
        each.edit_btn.destroy()
        each.delete_btn.destroy()
    my_relays = []

    it = 0
    for relay in my_file.get_relay_info():
        read_relay = Relays(it,
                            relay["Name"],
                            relay["IP"],
                            relay["Relay"],
                            relay["start"],
                            relay["end"],
                            relay["status"])
        my_relays.append(read_relay)
        it += 1
    draw_buttons()


def draw_buttons():
    relay_count = len(my_relays)
    this_relay = 0
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[0]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[0]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(0))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)
        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[1]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[1]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(1))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[2]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[2]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(2))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[3]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[3]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(3))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[4]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[4]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(4))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[5]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[5]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(5))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[6]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[6]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(6))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[7]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[7]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(7))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[8]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[8]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(8))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[9]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[9]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(9))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[10]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[10]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(10))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[11]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[11]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(11))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[12]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[12]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(12))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[13]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[13]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(13))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[14]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[14]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(14))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[15]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[15]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(15))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[16]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[16]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(16))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[17]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[17]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(17))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[18]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[18]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(18))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[19]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[19]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(19))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[20]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[20]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(20))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[21]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[21]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(21))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[22]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[22]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(22))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[23]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[23]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(23))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[24]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[24]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(24))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[25]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[25]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(25))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[26]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[26]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(26))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[27]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[27]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(27))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[28]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[28]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(28))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[29]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[29]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(29))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[30]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[30]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(30))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[31]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[31]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(31))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[32]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[32]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(32))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[33]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[33]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(33))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[34]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[34]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(34))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[35]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[35]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(35))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[36]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[36]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(36))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[37]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[37]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(37))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[38]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[38]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(38))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1
    if relay_count > 0:
        my_relays[this_relay].button = Button(tk,
                                              text=my_relays[this_relay].name + ":" + my_relays[
                                                  this_relay].get_status(),
                                              width=15, height=2, bg="grey",
                                              command=lambda: button_on_light(my_relays[39]))
        my_relays[this_relay].button.place(x=5 + (this_relay % 8) * 125, y=55 + (this_relay // 8) * 100)

        my_relays[this_relay].edit_btn = Button(tk,
                                                text="Edit",
                                                width=6, height=2,
                                                command=lambda: edit_button(my_relays[39]))
        my_relays[this_relay].edit_btn.place(x=5 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        my_relays[this_relay].delete_btn = Button(tk,
                                                  text="Delete",
                                                  width=7, height=2, bg="pink",
                                                  command=lambda: delete_button(39))
        my_relays[this_relay].delete_btn.place(x=61 + (this_relay % 8) * 125, y=100 + (this_relay // 8) * 100)

        relay_count -= 1
        this_relay += 1


draw_buttons()
while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.005)
