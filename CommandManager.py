from Manager import Manager

class CommandManager(Manager):
    def execute(self, cmd):
        state = self.all_managers[self.state.index][0]
        if (state == "Options"):
            if (cmd == "up"):
                self.manager.allowed_functions().shiftup()
            elif (cmd == "down"):
                self.manager.allowed_functions().shiftdown()
            elif (cmd == "right"):
                self.manager.allowed_functions().nextcol()
            elif (cmd == "left"):
                self.manager.allowed_functions().prevcol()
            else:
                raise Exception("Command \"" + cmd + "\" not recognized in " + state + " state.")
        elif (state == "Game"):
            if (cmd == "next"):
                self.manager.allowed_functions().next()
            elif (cmd[0:4] == "throw"):
                x = cmd.split
                if len(x) == 3:
                    self.manager.allowed_functions().throw_dart(x[1], x[2])
            else:
                raise Exception("Command \"" + cmd + "\" not recognized in " + state + " state.")
        elif (state == "Winner"):
            if (cmd == "done"):
                self.manager.allowed_functions().done()
        else:
            raise Exception("Unrecognized State: " + str(state))

if __name__ == '__main__':
    manager = CommandManager()
    while True:
        for i in manager.format_str(level = 0, indent = "  ").split("\n"):
            print i
        print("")
        cmd = raw_input("Command: ")
        print("Given: " + cmd)
        manager.execute(cmd)
