import tkinter as tk
import tkinter.ttk as ttk
import typing

from view.frames.BasicFrame import BasicFrame, RowFrame, RowFrameRow


def grid_position(index: int):
    if index == 0:
        return 0, 0
    else:
        index, r1 = divmod(index, 3)
        index, r2 = divmod(index, 3)
        return r2, r1


class DroneSelectionFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, navigation_buttons=True)

        # Title Label
        self.title_label = ttk.Label(self.frame, text='SELECT\nDRONES', anchor=tk.CENTER, font=('', 21))
        self.place_in_grid(self.title_label, (0, 0), (3, 3))

        # Drone grid frame
        self.drone_grid_frame = ttk.LabelFrame(self.frame, text='DRONES')
        self.drone_grid_frame_class = DroneGridFrame(self.drone_grid_frame)
        self.drone_grid_frame_class.pack_frame()
        self.place_in_grid(self.drone_grid_frame, (0, 4), (7, 15))


# DRONE GRID
class DroneGridFrame(BasicFrame):
    def __init__(self, master=None):
        super().__init__(master, grid=(2, 3))

        # Drone grid
        self.drone_grid = dict()
        self.grid_cols, self.grid_rows = self.grid(self.frame)

        # Blank drone add button callback event (PLACEHOLDER LAMBDA)
        self.blank_drone_callback: typing.Callable = lambda: print('Hi')

        # Init grid empty cells
        self.init_empty_grid()

        # TEST
        self.pack_cell(GlobalDroneCell(self.frame, 0), grid_position(0))
        self.pack_cell(LocalDroneCell(self.frame, 1), grid_position(1))
        self.pack_cell(DirectDroneCell(self.frame, 2), grid_position(2))

    def init_empty_grid(self):
        for nn in range(self.grid_cols*self.grid_rows):
            self.pack_cell(BlankDroneCell(self.frame, nn, callback=self.blank_drone_callback), grid_position(nn))

    def pack_cell(self, drone_cell, cell_index: typing.Tuple[int, int]):
        grid_key = f'{cell_index[0]}{cell_index[1]}'
        self.drone_grid[grid_key] = drone_cell
        self.place_in_grid(drone_cell.frame, cell_index)

    def cell_is_available(self, cell_index: typing.Tuple[int, int]):
        no_cell = f'{cell_index[0]}{cell_index[1]}' not in self.drone_grid
        if no_cell:
            return True
        else:
            empty_cell = self.drone_grid[f'{cell_index[0]}{cell_index[1]}'].empty
            return empty_cell

    def add_drone_cell(self, drone_cell):
        for ii_rows in self.grid_rows:
            for jj_cols in self.grid_cols:
                cell_index = (ii_rows, jj_cols)
                if self.cell_is_available(cell_index):
                    self.pack_cell(drone_cell, cell_index)


# # DRONE CELLS
class DroneCell(RowFrame):
    def __init__(self, master, drone_id: int):
        super().__init__(master, label=f'DRONE #{drone_id}')

        self.drone_id = drone_id

        self.add_options_row(DroneNameRow(self.frame))


# GLOBAL DRONE CELL
class GlobalDroneCell(DroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id)

        self.add_options_row(GlobalDroneCellRow(self.frame))

        self.pack_rows()


# LOCAL DRONE CELL
class LocalDroneCell(DroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id)

        self.add_options_row(LocalDroneIpEntryRow(self.frame))

        self.pack_rows()


# DIRECT DRONE CELL
class DirectDroneCell(DroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id)

        self.add_options_row(DirectDroneComRow(self.frame))

        self.pack_rows()


# BLANK DRONE CELL
class BlankDroneCell(BasicFrame):
    def __init__(self, master, drone_id: int, callback: typing.Callable = None):
        super().__init__(master, no_grid=True, label=f'DRONE #{drone_id}')
        self.callback = callback

        self.add_drone_label = ttk.Label(self.frame, text='⊕', anchor='center', font=('', 52))
        self.add_drone_label.bind('<Button-1>', self.on_add_drone_click)
        self.pack_widget(self.add_drone_label)

    def on_add_drone_click(self, event=None):
        self.callback()


# BASIC DRONE CELL ROW
class DroneNameRow(RowFrameRow):
    def __init__(self, master):
        super().__init__(master)

        self.name_entry_var = tk.StringVar()

        self.name_entry_label = ttk.Label(self.frame, text='NAME:')
        self.pack_widget(self.name_entry_label, 'left', 2)

        self.name_entry = ttk.Entry(self.frame, textvariable=self.name_entry_var)
        self.pack_widget(self.name_entry, 'right', 2)


# GLOBAL DRONE CELL ROWS
class GlobalDroneCellRow(RowFrameRow):
    def __init__(self, master):
        super().__init__(master)


# LOCAL DRONE CELL
class LocalDroneIpEntryRow(RowFrameRow):
    def __init__(self, master):
        super().__init__(master)

        self.ip_entry_var = tk.StringVar()

        self.ip_entry_label = ttk.Label(self.frame, text='IP ADDRESS:')
        self.pack_widget(self.ip_entry_label, 'left', 2)

        self.ip_entry = ttk.Entry(self.frame, textvariable=self.ip_entry_var)
        self.pack_widget(self.ip_entry, 'right', 2)


# DIRECT DRONE CELL
class DirectDroneComRow(RowFrameRow):
    def __init__(self, master):
        super().__init__(master)

        self.com_entry_var = tk.IntVar()

        self.com_entry_label = ttk.Label(self.frame, text='COM PORT NUMBER:')
        self.pack_widget(self.com_entry_label, 'left', 2)

        self.com_entry = ttk.Entry(self.frame, textvariable=self.com_entry_var)
        self.pack_widget(self.com_entry, 'right', 2)


if __name__ == '__main__':
    import view.MyTk as MyTk

    win = MyTk.Window()
    win.config()
    DroneSelectionFrame(win).pack_frame()
    win.mainloop()
