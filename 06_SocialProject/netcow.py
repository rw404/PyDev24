import cmd
import readline
import shlex
import socket
import threading


class NetCow(cmd.Cmd):
    def __init__(self, socket: socket.socket) -> None:
        super().__init__()
        self.sock = socket
        self.completion = None
        self.alive: bool = True
        self.logged: bool = False

    def parse_shlex(self, args):
        split_args = shlex.split(args)
        if len(split_args) == 0:
            split_args = [""]

        return split_args

    def do_who(self, arg):
        """
        Returns logged cows
        Usage: who
        """
        self.request("who")

    def do_cows(self, arg):
        """
        Returns logged cows
        Usage: cows
        """
        self.request("cows")

    def do_login(self, name):
        """
        Creates session for user with [name] identificator
        Usage: login [name]

        Params:
            name[REQUIRED]: string name
        """
        self.request(f"login {name}")

    def complete_login(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()
        self.request("complete_cows")
        while self.completion is None:
            pass

        completion_list = [line.strip() for line in self.completion.split()[1:]]

        if words[-1] != "login":
            completion_list = [
                line for line in completion_list if line.startswith(words[-1])
            ]
            if len(completion_list) == 0:
                completion_list = None
        self.completion = None

        return completion_list

    def do_say(self, args):
        """
        Say [cow_msg] [cow_name] identificator
        Usage: say [cow_msg] [cow_name]

        Params:
            cow_name[REQUIRED]: string name of logged cow
            cow_msg[REQUIRED]: string message
        """
        parsed_args = self.parse_shlex(args)
        self.request(f"say {parsed_args[0]} {parsed_args[1]}")

    def complete_say(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()
        self.request("complete_who")
        while self.completion is None:
            pass

        completion_list = [line.strip() for line in self.completion.split()[1:]]

        if words[-1] != "say":
            completion_list = [
                line for line in completion_list if line.startswith(words[-1])
            ]
            if len(completion_list) == 0:
                completion_list = None
        self.completion = None

        return completion_list

    def do_yield(self, message):
        """
        Send all users your message
        Usage: yield [message]

        Params:
            message[REQUIRED]: string message
        """
        self.request(f"yield {message}")

    def do_quit(self, arg):
        """
        End session
        Usage: quit
        """
        self.alive = False
        if not self.logged:
            self.sock.shutdown(socket.SHUT_WR)
        else:
            self.request("quit")

        return True

    def receive(self):
        while self.alive:
            get_data = self.sock.recv(1024).decode()

            if get_data.startswith("compl"):
                self.completion = get_data
            elif get_data.startswith("quit"):
                break
            elif get_data.strip().startswith("Empty message"):
                pass
            else:
                if get_data.strip().startswith(
                    "You've logged in succesfully with cow name:"
                ):
                    self.logged = True
                print(
                    f"\n{get_data.strip()}\n{self.prompt}{readline.get_line_buffer()}",
                    end="",
                    flush=True,
                )

    def request(self, message: str):
        self.sock.send(f"{message}\n".encode())


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(("0.0.0.0", 1337))
        netcow = NetCow(client_socket)
        timer = threading.Thread(target=netcow.receive, args=())
        timer.start()
        netcow.cmdloop()
