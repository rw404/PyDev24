import cmd
import shlex

import cowsay


class CowSayShell(cmd.Cmd):
    def parse_shlex(self, args):
        split_args = shlex.split(args)
        if len(split_args) == 0:
            split_args = [""]

        return split_args

    def do_cowthink(self, args):
        """
        Cowthink programm
        Usage: cowthink [message] [-f cowfile] [-e eyes] [-T tongue]

        Params:
            message[REQUIRED]: string message
            -f[OPTIONAL]: one of list_cows
            -e[OPTIONAL]: cow eyes, 2 first letters are used
            -T[OPTIONAL]: two letter cow's tongue
        """
        splitted_args = self.parse_shlex(args)

        cowsay_params = {
            "message": splitted_args[0],
            "cow": "default",
            "eyes": cowsay.Option.eyes,
            "tongue": cowsay.Option.tongue,
        }

        if len(splitted_args) > 1:
            for param, next_param in zip(splitted_args[:-1], splitted_args[1:]):
                match param:  # noqa: E999 - ignore match case flake8 error
                    case "-f":
                        cowsay_params["cow"] = next_param
                    case "-e":
                        cowsay_params["eyes"] = next_param
                    case "-T":
                        cowsay_params["tongue"] = next_param

        print(cowsay.cowthink(**cowsay_params))

    def complete_cowthink(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()

        match words[-1]:
            case "-e":
                return [eye.eyes for eye in cowsay.COW_OPTIONS.values()]
            case "-T":
                return [tongue.tongue for tongue in cowsay.COW_OPTIONS.values()]
        return None

    def do_cowsay(self, args):
        """
        Cowsay programm
        Usage: cowsay [message] [-f cowfile] [-e eyes] [-T tongue]

        Params:
            message[REQUIRED]: string message
            -f[OPTIONAL]: one of list_cows
            -e[OPTIONAL]: cow eyes, 2 first letters are used
            -T[OPTIONAL]: two letter cow's tongue
        """
        splitted_args = self.parse_shlex(args)

        cowsay_params = {
            "message": splitted_args[0],
            "cow": "default",
            "eyes": cowsay.Option.eyes,
            "tongue": cowsay.Option.tongue,
        }

        if len(splitted_args) > 1:
            for param, next_param in zip(splitted_args[:-1], splitted_args[1:]):
                match param:  # noqa: E999 - ignore match case flake8 error
                    case "-f":
                        cowsay_params["cow"] = next_param
                    case "-e":
                        cowsay_params["eyes"] = next_param
                    case "-T":
                        cowsay_params["tongue"] = next_param

        print(cowsay.cowsay(**cowsay_params))

    def complete_cowsay(self, text, line, begidx, endidx):
        words = (line[:endidx]).split()

        match words[-1]:
            case "-e":
                return [eye.eyes for eye in cowsay.COW_OPTIONS.values()]
            case "-T":
                return [tongue.tongue for tongue in cowsay.COW_OPTIONS.values()]
        return None

    def do_list_cows(self, args):
        """
        Print list of cows:
        Usage: list_cows [file]

        Params:
            file[OPTIONAL]: files of list
        """

        list_cows_args = self.parse_shlex(args)
        if list_cows_args[0] == "":
            list_cows_args[0] = cowsay.COW_PEN

        print(cowsay.list_cows(*list_cows_args))

    def do_make_bubble(self, args):
        """
        Make bubble programm
        Usage: make_bubble [message]

        Params:
            message[REQUIRED]: string message
        """
        bubble_args = self.parse_shlex(args)

        print(cowsay.make_bubble(*bubble_args))

    def do_exit(self, *args):
        """
        Call to exit
        """
        return True


if __name__ == "__main__":
    cowsayshell = CowSayShell()
    cowsayshell.cmdloop()
