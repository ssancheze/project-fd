"""
Main race tester to use alongside MP's SITL and a locally hosted external broker. Currently does: \n
1. Adds one Player(number=33, icon='blue) \n
2. Selects the track circuit_default.waypoints \n
3. Loads the race frame with the track, starting point and player. \n
(SOMETIMES THE PLAYER MAY NOT APPEAR DUE TO DRONEKIT BEING UNABLE TO GET THEIR DRONE TELEMETRY) \n
FOR THE FULL PROGRAM SEQUENCE SEE THE SCRIPT BELOW ALONGSIDE WITH THE FLOWCHART DIAGRAM PROVIDED IN
'assets/pfd_flowchart.svg'
AS WELL AS HERE:
https://drive.google.com/file/d/1WOaJ9b56xLq72rXsyrmuDda5cW1Wb5Z2/view?usp=sharing (contenido/uml/pfd_flowchart.svg) \n
Upon pressing the button «All Players Ready» the program will start its race sequence (printed on console): \n
1. After some time, the drone will take of to its race height and go to the starting point. \n
2. When it does, a countdown will be printed on console. \n
3. When it reaches 0, the drone's tracker will start (along with the message 'GO!' on console) \n
4. After that, the player may go around the circuit completing as many laps as they want. Crossing checkpoints and
completing laps will be registered, and a message on console will be printed. \n
There is no ending sequence. Closing the application will terminate both the SITL and the broker connection.
"""
from view.MyTk import Window
from view.frames.maps.RaceViewFrame import RaceViewFrame
from model.managers.PlayerManager import PlayerManager
from model.managers.CommsManager import CommsManager
from model.managers.TrackManager import TrackManager
from model.managers.FlightManager import FlightManager
from model.managers.RaceManager import RaceManager
from model.utils import rotate_list


def main2():
    comms_manager = CommsManager()
    comms_manager.simulation_mode()

    player_manager = PlayerManager(comms_manager)
    player_manager.add_player(33, 'blue')
    player_manager.link_communication_handler(33)

    track_manager = TrackManager()
    track_manager.select_track('circuit_default.waypoints', len(player_manager.players_list))

    flight_manager = FlightManager(player_manager, track_manager)
    flight_manager.link_autopilot_controller(33)

    player_starting_point = track_manager.race_model.starting_points.starting_points.pop()
    player_starting_zone_absolute = track_manager.race_model.starting_points.starting_zones.pop()
    flight_manager.link_seeker(33, player_starting_point, player_starting_zone_absolute)

    player_manager.link_stopwatch(33)

    player_checkpoints = rotate_list(track_manager.race_model.checkpoints, player_starting_zone_absolute)
    player_zone_lengths = rotate_list(track_manager.race_model.starting_points.track_length.lengths,
                                      player_starting_zone_absolute)

    player_manager.link_tracker(33, flight_manager.autopilot_controllers[33].telemetry_info,
                                player_checkpoints, player_zone_lengths)

    race_manager = RaceManager(player_manager, track_manager, flight_manager)

    window = Window()
    window.config()

    race_view = RaceViewFrame(window, race_manager.race_controller)
    race_manager.bind_race_view(race_view)

    race_view.map_class.control_frame.draw_update()

    flight_manager.autopilot_controllers[33].vehicle_connect()
    flight_manager.bind_telemetries(race_view.map_class.control_frame.racer_update)

    window.mainloop()

    # input('Press Enter to exit')


if __name__ == '__main__':
    main2()
