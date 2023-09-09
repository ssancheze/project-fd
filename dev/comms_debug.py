from time import sleep

from model.services.AutopilotServiceMini import AutopilotServiceMini
from model.services.MQTTMessageHandler import AutopilotServiceController
from model.services.CommunicationModeHandler import CommunicationModeHandler

ctrl_comms = CommunicationModeHandler('ProjectFD', 0)
ctrl_comms.sim_mode()
aps_comms = CommunicationModeHandler('AutopilotServiceMini', 0)
aps_comms.sim_mode()


ctrl = AutopilotServiceController(ctrl_comms, 0)
aps = AutopilotServiceMini(aps_comms)

sleep(0.1)
ctrl.vehicle_connect()
ctrl.vehicle_arm()
ctrl.vehicle_take_off(5)
input()
