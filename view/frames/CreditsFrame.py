import tkinter
import tkinter.ttk as ttk

from view.frames.BasicFrame import BasicFrame
from controller.FrameControllers import CreditsFrameController


class CreditsFrame(BasicFrame):
    def __init__(self, master, controller: CreditsFrameController):
        super().__init__(master, navigation_buttons=True)

        self.controller: CreditsFrameController = controller

        # Start Button
        self.text(self.nav_right_button, 'START')
        self.nav_right_button.config(command=self.start_button_click)

        # Settings Button
        self.text(self.nav_left_button, 'SETTINGS')
        self.nav_left_button.config(command=self.settings_button_click)

        # Credits Button
        self.text(self.nav_center_button, 'CREDITS')
        self.nav_center_button.config(command=self.credits_button_click)

        # Credits frame
        self.zero_credits_class = VersionZeroCredits(self.frame)
        self.place_in_grid(self.zero_credits_class.frame, (0, 0), (0, 15), 10)

    def start_button_click(self):
        self.controller.right_button_click()

    def settings_button_click(self):
        self.controller.left_button_click()

    def credits_button_click(self):
        self.controller.top_button_click()


class VersionZeroCredits(BasicFrame):
    def __init__(self, master):
        super().__init__(master, no_grid=True)

        self.version_label = ttk.Label(
            text='Version 0.33', font=('', 0, 'bold'),
            anchor=tkinter.CENTER
        )
        self.pack_widget(self.version_label, 'top', 3)

        self.dev_label = ttk.Label(
            text='SOLE DEVELOPER Sergio Sánchez Eraso',
            anchor=tkinter.CENTER
        )
        self.pack_widget(self.dev_label, 'top', 3)

        self.manager_label = ttk.Label(
            text='PROJECT RESPONSIBLE Miguel Valero García',
            anchor=tkinter.CENTER
        )
        self.pack_widget(self.manager_label, 'top', 3)


if __name__ == '__main__':
    import view.MyTk as MyTk
    from model.FrameModels import CreditsFrameModel
    mdl = CreditsFrameModel()
    ctrl = CreditsFrameController(mdl)

    win = MyTk.Window()
    win.config()
    foo = CreditsFrame(win, ctrl)
    foo.pack_frame()
    win.mainloop()
