import pywintypes
import sys
import time
import win32file
import win32pipe


class Pipe:
    def __init__(self, server):
        if server:
            self.server = True
            self.client = False
            self.pipe = win32pipe.CreateNamedPipe(
                r'\\.\pipe\Foo',
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE |
                win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None
            )
        else:
            self.server = False
            self.client = True
            self.pipe = None

    def pipe_server(self):
        # print("waiting for client")
        win32pipe.ConnectNamedPipe(self.pipe, None)
        # print("got client")

        message = []
        while len(message) < 4:
            # print(f"reading message")
            resp = win32file.ReadFile(self.pipe, 64*1024)[1]
            resp = int.from_bytes(resp, "little")
            message.append(resp)
            # print(f"message: {message}")
        yield message

    def close_handle(self):
        return win32file.CloseHandle(self.pipe)

    def pipe_client(self):
        if self.client:
            print("pipe client")
            quit = False

            while not quit:
                try:
                    handle = win32file.CreateFile(
                        r'\\.\pipe\Foo',
                        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                        0,
                        None,
                        win32file.OPEN_EXISTING,
                        0,
                        None
                    )
                    res = win32pipe.SetNamedPipeHandleState(
                        handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
                    if res == 0:
                        print(f"SetNamedPipeHandleState return code: {res}")

                    count = 0
                    while count < 10:
                        print(f"writing message {count}")
                        # convert to bytes
                        some_data = str.encode(f"{count}")
                        win32file.WriteFile(handle, some_data)
                        # time.sleep(1)
                        count += 1
                except pywintypes.error as e:
                    if e.args[0] == 2:
                        print("no pipe, trying again in a sec")
                        time.sleep(1)
                    elif e.args[0] == 109:
                        print("broken pipe, bye bye")
                        quit = True
        else:
            raise Exception


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("need s or c as argument")
    elif sys.argv[1] == "s":
        pipe = Pipe(server=True)
        for message in pipe.pipe_server():
            print(message)
    elif sys.argv[1] == "c":
        pipe = Pipe(server=False)
        pipe.pipe_client()
    elif sys.argv[1] == "x":
        pipe = Pipe(server=True)
        pipe.close_handle()
    else:
        print(f"no can do: {sys.argv[1]}")