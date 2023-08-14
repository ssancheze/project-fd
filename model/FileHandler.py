import typing


class FileHandler:
    def __init__(self, filepath: str, separator: typing.Optional[str] = None, overwrite: bool = False):
        self._file_writer = FileWriter(filepath, separator, overwrite)
        self._file_reader = FileReader(filepath, separator)

        with open(filepath, 'r') as _file:
            _count = 0
            while True:
                _line = _file.readline()
                if _line:
                    _count += 1
                else:
                    break

            self._line_count = _count

    @property
    def file_reader(self):
        return self._file_reader

    @property
    def file_writer(self):
        return self._file_writer

    @property
    def line_count(self):
        return self._line_count

    def read(self, line: int, column: typing.Optional[int] = None):
        if line < 0:
            _line = self._line_count + line
        else:
            _line = line

        if column is not None:
            return self._file_reader.readblock(_line, column)
        else:
            return self._file_reader.readline(_line)

    def write(self, line: typing.Union[str, typing.List[str]]):
        self._file_writer.writeline(line)


class FileOpener:
    _encoding = 'utf-8'

    def __init__(self, filepath: str, mode: str):
        self._filepath = filepath
        self._mode = mode
        with self.open as _:
            pass

    @property
    def open(self):
        return open(self._filepath, self._mode, encoding=self.__class__._encoding)


class FileReader(FileOpener):
    def __init__(self, filepath: str, separator: typing.Optional[str] = None):
        FileOpener.__init__(self, filepath, 'r')

        self._line = None
        self._col = None
        self._buffer = None
        self._separator = separator

    def readline(self, line: int):
        if self._line == line and self._col is None:
            return self._buffer
        else:
            with self.open as file:
                for _index, _line in enumerate(file):
                    if _index == line:
                        if _line.endswith('\n'):
                            _line = _line.strip('\n')
                        self._line = _index
                        self._buffer = _line
                        self._col = None
                        return _line

    def readblock(self, line: int, column: int):
        if self._line == line:
            if self._col == column:
                return self._buffer
            elif self._col is None:
                _line = self._buffer
            else:
                _line = self.readline(line)
        else:
            _line = self.readline(line)

        if self._separator is not None:
            _block = _line.split(self._separator)[column]
        else:
            _block = _line[column]

        self._line = line
        self._col = column
        self._buffer = _block
        return _block


class FileWriter(FileOpener):
    def __init__(self, filepath: str, separator: typing.Optional[str] = None, overwrite: bool = False):
        if overwrite is True:
            mode = 'w'
        else:
            mode = 'a'
        self._separator = separator
        self._written = False

        FileOpener.__init__(self, filepath, mode)

    def writeline(self, line: typing.Union[str, typing.List[str]]):
        if isinstance(line, list):
            _line = self._separator.join(line)
        else:
            _line = line

        if not _line.endswith('\n'):
            _line += '\n'

        with self.open as _file:
            _file.write(_line)


if __name__ == '__main__':
    my_handler = FileHandler('../dev/fence_test4.waypoints', separator='\t')
    print(my_handler.read(0))
