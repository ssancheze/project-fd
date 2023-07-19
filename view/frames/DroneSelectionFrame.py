import tkinter as tk
import tkinter.ttk as ttk
import typing

from view.frames.BasicFrame import BasicFrame


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

        # Init grid empty cells
        self.init_empty_grid()

        # TEST
        self.pack_cell(GlobalDroneCell(self.frame, 0), grid_position(0))
        self.pack_cell(LocalDroneCell(self.frame, 1), grid_position(1))
        self.pack_cell(DirectDroneCell(self.frame, 2), grid_position(2))

    def init_empty_grid(self):
        for nn in range(self.grid_cols*self.grid_rows):
            self.pack_cell(BasicDroneCell(self.frame, nn, callback=lambda: print('Hi')), grid_position(nn))

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


# BASIC DRONE CELL
class BasicDroneCell(BasicFrame):
    def __init__(self, master, drone_id: int, empty=True, callback: typing.Callable = None):
        super().__init__(master, no_grid=True, label=f'DRONE #{drone_id}')
        self.empty = empty
        self.callback = callback

        if empty:
            self.add_drone_label = ttk.Label(self.frame, text='⊕', anchor='center', font=('', 52))
            self.add_drone_label.bind('<Button-1>', self.on_add_drone_click)
            self.pack_widget(self.add_drone_label)

    def on_add_drone_click(self, event=None):
        self.callback()


# GLOBAL DRONE CELL
class GlobalDroneCell(BasicDroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id, empty=False)


# LOCAL DRONE CELL
class LocalDroneCell(BasicDroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id, empty=False)

        # IP Entry
        self.ip_entry_var = tk.StringVar()

        self.ip_entry_label = ttk.Label(self.frame, text='IP ADDRESS:')
        self.pack_widget(self.ip_entry_label, 'left', 2)

        self.ip_entry = ttk.Entry(self.frame, textvariable=self.ip_entry_var)
        self.pack_widget(self.ip_entry, 'right', 2)


# DIRECT DRONE CELL
class DirectDroneCell(BasicDroneCell):
    def __init__(self, master, drone_id: int):
        super().__init__(master, drone_id, empty=False)

        # COM Entry
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
