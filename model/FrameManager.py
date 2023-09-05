import tkinter
import typing

from view.frames import BasicFrame, WelcomeFrame, CreditsFrame, ModeSelectionFrame
from controller import FrameControllers
from model import FrameModels


class FrameManager(BasicFrame.BasicFrame):
    def __init__(self, master):
        """
        All frames belong in the same window. To switch to a frame, the tkinter function raise is called.
        :param master:
        """
        super().__init__(master, no_grid=True)

        self.container = tkinter.Frame(self.frame)

        self.frames: typing.Dict[str, BasicNavManager] = {}
        for F in (WelcomeManager, CreditsManager, ModeSelectionManager):
            frame_name = F.__name__
            frame = F(self.container)
            self.frames[frame_name] = frame

        self.show_frame("WelcomeManager")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.view.frame.tkraise()


class BasicNavManager:
    def __init__(self):
        self.model = None
        self.controller = None
        self.view = None
        
    def nav_buttons_callback(self, right_callback, left_callback, top_callback):
        self.model.set_callback('right', right_callback)
        self.model.set_callback('left', left_callback)
        self.model.set_callback('top', top_callback)

    def raise_frame(self):
        self.__raise_frame()

    @staticmethod
    def __raise_frame():
        def wrapper(self):
            self.view.frame.tkraise()

        return wrapper


class WelcomeManager(BasicNavManager):
    def __init__(self, master):
        super().__init__()
        self.model = FrameModels.WelcomeFrameModel()
        self.controller = FrameControllers.WelcomeFrameController(self.model)
        self.view = WelcomeFrame.WelcomeFrame(master, self.controller)
        self.view.pack_frame()


class CreditsManager(BasicNavManager):
    def __init__(self, master):
        super().__init__()
        self.model = FrameModels.CreditsFrameModel()
        self.controller = FrameControllers.CreditsFrameController(self.model)
        self.view = CreditsFrame.CreditsFrame(master, self.controller)
        self.view.pack_frame()


class ModeSelectionManager(BasicNavManager):
    def __init__(self, master):
        super().__init__()
        self.model = FrameModels.ModeSelectionFrameModel()
        self.controller = FrameControllers.ModeSelectionFrameController(self.model)
        self.view = ModeSelectionFrame.ModeSelectionFrame(master, self.controller)
        self.view.pack_frame()


if __name__ == '__main__':
    import view.MyTk as MyTk

    win = MyTk.Window()
    win.config()

    foo = FrameManager(win)
    foo.pack_frame()
    win.mainloop()
