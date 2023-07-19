import typing
from view.frames.BasicFrame import BasicFrame
import tkinter.ttk as ttk
import tkinter as tk


class ModeSelectionFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, navigation_buttons=True)

        # Title Label
        self.title_label = ttk.Label(self.frame, text='SELECT\nMODE', anchor=tk.CENTER, font=('', 21))
        self.place_in_grid(self.title_label, (0, 1), (2, 4))

        # Global button
        self.global_button = ttk.Button(self.frame, text='GLOBAL')
        self.place_in_grid(self.global_button, (3, 1), (3, 4))

        # Local button
        self.local_button = ttk.Button(self.frame, text='LOCAL')
        self.place_in_grid(self.local_button, (4, 1), (4, 4))

        # Direct button
        self.direct_button = ttk.Button(self.frame, text='DIRECT')
        self.place_in_grid(self.direct_button, (5, 1), (5, 4))

        # Options frame
        self.global_options_frame = GlobalModeOptionsFrame(self.frame, 10, label='GLOBAL OPTIONS')
        self.place_in_grid(self.global_options_frame.frame, (0, 6), (1, 15))

        self.local_options_frame = LocalModeOptionsFrame(self.frame, 10, label='LOCAL OPTIONS')
        self.place_in_grid(self.local_options_frame.frame, (2, 6), (3, 15))

        self.direct_options_frame = DirectModeOptionsFrame(self.frame, 10, label='DIRECT OPTIONS')
        self.place_in_grid(self.direct_options_frame.frame, (4, 6), (5, 15))


# OPTIONS ROW AND FRAME TEMPLATES
class ModeOptionsRow(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, no_grid=True)

        self.frame.configure(relief='groove', borderwidth=3)


class ModeOptionsFrame(BasicFrame):
    def __init__(self, master=None, rows=1, label: str = None):
        super().__init__(master, no_grid=True, label=label)

        self.rows = rows
        self.options_rows_list: typing.List[ModeOptionsRow] = list()

    def add_options_row(self, mode_options_row: ModeOptionsRow):
        if len(self.options_rows_list) > self.rows:
            raise IndexError(f'self.options_rows_list try to exceed maximum length')
        else:
            self.options_rows_list.append(mode_options_row)

    def pack_rows(self):
        for row in self.options_rows_list:
            row.pack_frame(side='top', fill='x')


# GLOBAL MODE OPTION ROWS
class BrokerAddressOptionRow(ModeOptionsRow):
    def __init__(self, master=None):
        super().__init__(master)

        # Broker Address label
        self.broker_address_label = ttk.Label(self.frame, text='BROKER ADDRESS:')
        self.pack_widget(self.broker_address_label, 'left', 2)

        # Broker Address dropdown
        self.broker_address_dropdown_var = tk.StringVar()
        self.broker_address_dropdown = ttk.OptionMenu(self.frame, self.broker_address_dropdown_var)
        self.pack_widget(self.broker_address_dropdown, 'right', 2)

        # Informative label
        self.info_label = ttk.Label(self.frame, text='or select from the list:')
        self.pack_widget(self.info_label, 'right', 2)

        # Broker Address text field
        self.broker_address_text_field_var = tk.StringVar()
        self.broker_address_text_field = ttk.Entry(self.frame, textvariable=self.broker_address_text_field_var,)
        self.pack_widget(self.broker_address_text_field, 'right', 2)

        self.broker_address_dropdown.configure(width=self.broker_address_text_field.cget('width') - 5)


class BrokerCredentialsOptionRow(ModeOptionsRow):
    def __init__(self, master=None):
        super().__init__(master)

        # Title label
        self.title_label = ttk.Label(self.frame, text='BROKER CREDENTIALS:')
        self.pack_widget(self.title_label, 'left', 2)

        # Password text field
        self.pwd_text_field_var = tk.StringVar(self.frame)
        self.pwd_text_field = ttk.Entry(self.frame, textvariable=self.pwd_text_field_var)
        self.pack_widget(self.pwd_text_field, 'right', 2)

        self.pwd_info_label = ttk.Label(self.frame, text='Password:')
        self.pack_widget(self.pwd_info_label, 'right', 2)

        # Username text field
        self.usr_text_field_var = tk.StringVar(self.frame)
        self.usr_text_field = ttk.Entry(self.frame, textvariable=self.usr_text_field_var)
        self.pack_widget(self.usr_text_field, 'right', 2)

        self.usr_info_label = ttk.Label(self.frame, text='Username:')
        self.pack_widget(self.usr_info_label, 'right', 2)


# LOCAL MODE OPTION ROWS
class LocalSubmodeOptionRow(ModeOptionsRow):
    def __init__(self, master=None):
        super().__init__(master)

        self.title_label = ttk.Label(self.frame, text='LOCAL SUB-MODE:')
        self.pack_widget(self.title_label, 'left', 2)

        self.submode_var = tk.IntVar(self.frame)
        self.single_radiobutton = ttk.Radiobutton(self.frame, text='Single broker', variable=self.submode_var,
                                                  value=0)
        self.pack_widget(self.single_radiobutton, 'right', 2)

        self.onboard_radiobutton = ttk.Radiobutton(self.frame, text='Onboard broker', variable=self.submode_var,
                                                   value=1)
        self.pack_widget(self.onboard_radiobutton, 'right', 2)


#  GLOBAL / LOCAL / DIRECT FRAMES
class GlobalModeOptionsFrame(ModeOptionsFrame):
    def __init__(self, master=None, rows: int = 1, label: str = None):
        super().__init__(master, rows, label)

        self.add_options_row(BrokerAddressOptionRow(self.frame))
        self.add_options_row(BrokerCredentialsOptionRow(self.frame))

        self.pack_rows()


class LocalModeOptionsFrame(ModeOptionsFrame):
    def __init__(self, master=None, rows: int = 1, label: str = None):
        super().__init__(master, rows, label)

        self.add_options_row(LocalSubmodeOptionRow(self.frame))

        self.pack_rows()


class DirectModeOptionsFrame(ModeOptionsFrame):
    def __init__(self, master=None, rows: int = 1, label: str = None):
        super().__init__(master, rows, label)


#  MAIN BLOCK
if __name__ == '__main__':
    import view.MyTk as MyTk

    win = MyTk.Window()
    win.config()
    ModeSelectionFrame(win).pack_frame()
    win.mainloop()
