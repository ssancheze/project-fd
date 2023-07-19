import tkinter
from view.frames.BasicFrame import BasicFrame
import tkinter.ttk as ttk


class WelcomeFrame(BasicFrame):
    def __init__(self, master=None):
        # Parent class init
        super().__init__(master, navigation_buttons=True)

        # Title Label
        self.title_label = ttk.Label(self.frame, text='  PROJECT-FD\nPLACEHOLDER', anchor=tkinter.CENTER, font=('', 25))
        self.place_in_grid(self.title_label, (0, 0), (7, 15))

        # Start Button
        self.text(self.nav_right_button, 'START')

        # Settings Button
        self.text(self.nav_left_button, 'SETTINGS')

        # Credits Button
        self.text(self.nav_center_button, 'CREDITS')


if __name__ == '__main__':
    import view.MyTk as MyTk
    my_master = MyTk.Window()
    my_master.config()
    WelcomeFrame(my_master).pack_frame()
    my_master.mainloop()
