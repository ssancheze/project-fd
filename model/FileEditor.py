import typing


class FileEditor:
    _encoding = 'utf-8'
    _mode_dict = {
        'read': 'r',
        'append': 'a',
        'write': 'w',
        'create': 'x'
    }

    def __init__(self, filepath: str):
        self._filepath = filepath

    def _open(self, mode: str):
        _mode = self._mode_dict[mode]
        return open(self._filepath, _mode, encoding=self._encoding)

    def read_file(self):
        with self._open('read') as _file:
            return _file.readlines()

    def readline(self, line_index: int) -> str:
        with self._open('read') as _file:
            for _index, _line in enumerate(_file):
                if _index == line_index:
                    return _line

    def read_last_line(self):
        with self._open('read') as _file:
            _prev_line = ''
            _line = _file.readline()
            while _line:
                _prev_line = _line
                _line = _file.readline()
            return _prev_line

    def writeline(self, line: str, index: typing.Optional[int] = None):
        if index is None:
            with self._open('append') as _file:
                _file.write(line)
        else:
            with self._open('read') as _file:
                _data = _file.readlines()

            _data[index] = line
            with self._open('write') as _file:
                _file.writelines(_data)

    def clear_file(self):
        self._open('write').close()

    @property
    def len(self):
        with self._open('read') as _file:
            return sum(1 for _ in _file)


if __name__ == '__main__':
    import definitions
    import os.path
    fence_name = 'fence_test.waypoints'
    my_filepath = os.path.join(definitions.FENCES_DIR, fence_name)
    foe = FileEditor(my_filepath)
    header = foe.read_last_line()
    print(header)
