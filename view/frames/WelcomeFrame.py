import tkinter
import tkinter.ttk as ttk

from view.frames.BasicFrame import BasicFrame
from controller.FrameControllers import WelcomeFrameController


class WelcomeFrame(BasicFrame):
    def __init__(self, master=None, controller: WelcomeFrameController = None):
        # Parent class init
        super().__init__(master, navigation_buttons=True)

        self.controller = controller

        # Title Label
        self.title_label = ttk.Label(self.frame, text='  PROJECT-FD\nPLACEHOLDER', anchor=tkinter.CENTER, font=('', 25))
        self.place_in_grid(self.title_label, (0, 0), (7, 15))

        # Start Button
        self.text(self.nav_right_button, 'START')
        self.nav_right_button.config(command=self.start_button_click)

        # Settings Button
        self.text(self.nav_left_button, 'SETTINGS')

        # Credits Button
        self.text(self.nav_center_button, 'CREDITS')

    def start_button_click(self):
        self.controller.right_button_click()

    def settings_button_click(self):
        self.controller.top_button_click()

    def credits_button_click(self):
        self.controller.left_button_click()


if __name__ == '__main__':
    import view.MyTk as MyTk
    my_master = MyTk.Window()
    my_master.config()
    WelcomeFrame(my_master).pack_frame()
    my_master.mainloop()
