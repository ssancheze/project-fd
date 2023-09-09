import dev.race_debug
from view.frames.maps import MapViewFrame, MapViewControlFrames
from view.MyTk import Window


if __name__ == '__main__':
    action = input('Select action: ("race", "editor" -without quotes-): ')
    if action == 'race':
        dev.race_debug.main2()
    elif action == 'editor':
        win = Window()
        win.config()
        MapViewFrame.MapViewFrame(win, MapViewControlFrames.MapFenceEditorControlFrame)
        win.mainloop()
