"""
File for testing MQTT broker message sending to the AutopilotServiceMini
"""
import tkinter
import json

from model.services.CommunicationModeHandler import MQTTClientHandler

FROM_NAME = 'ProjectFD'
TO_NAME = 'AutopilotServiceMini'
DRONE_ID = 0
BROKER_ADDRESS = ('localhost', 8000)


class Debugger:
    def __init__(self):
        self.mqtt_client = MQTTClientHandler(FROM_NAME, TO_NAME, DRONE_ID)
        self.mqtt_client.connect_external(*BROKER_ADDRESS)

        self.root = tkinter.Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)

        self.connect_button = tkinter.Button(self.root, text='connect', command=self.connect)
        self.connect_button.grid(row=0, column=0)

        self.disconnect_button = tkinter.Button(self.root, text='disconnect', command=self.disconnect)
        self.disconnect_button.grid(row=1, column=0)

        self.arm_button = tkinter.Button(self.root, text='arm', command=self.arm)
        self.arm_button.grid(row=2, column=0)

        self.takeoff_button = tkinter.Button(self.root, text='take off', command=self.take_off)
        self.takeoff_button.grid(row=3, column=0)

        self.takeoff_var = tkinter.StringVar(self.root)
        self.takeoff_box = tkinter.Entry(self.root, textvariable=self.takeoff_var)
        self.takeoff_box.grid(row=3, column=1)

        self.goto_button = tkinter.Button(self.root, text='go to', command=self.go_to)
        self.goto_button.grid(row=4, column=0)

        self.goto_var = tkinter.StringVar(self.root)
        self.goto_box = tkinter.Entry(self.root, textvariable=self.goto_var)
        self.goto_box.grid(row=4, column=1)

        self.rtl_button = tkinter.Button(self.root, text='rtl', command=self.rtl)
        self.rtl_button.grid(row=5, column=0)

        self.root.mainloop()

    def connect(self):
        self.mqtt_client.publish_external('connect')

    def disconnect(self):
        self.mqtt_client.publish_external('disconnect')

    def arm(self):
        self.mqtt_client.publish_external('armDrone')

    def take_off(self):
        _payload = {'target_height': float(self.takeoff_var.get())}
        self.mqtt_client.publish_external('takeOff', json.dumps(_payload))

    def go_to(self):
        coordss = self.goto_var.get().split(',')
        coords = coordss[0].strip(' '), coordss[1].strip(' ')
        _payload = {'lat': float(coords[0]), 'lon': float(coords[1]), 'height': None}
        self.mqtt_client.publish_external('goTo', json.dumps(_payload))

    def rtl(self):
        self.mqtt_client.publish_external('returnToLaunch')


if __name__ == '__main__':
    foo = Debugger()
    foo.root.mainloop()
