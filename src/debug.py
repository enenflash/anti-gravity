class DebugConsole:
    def __init__(self, gamehost):
        self.gamehost = gamehost

        self.command_list = {
            "exit": "print('[%] Exiting Debug Console'",
            "commands": "print('  !', [command for command in self.command_list]",
            "hello_world": "self.test_method(",
            "addition": "self.test_method_2("
        }

    def test_method(self):
        print("  ! Hello World")

    def test_method_2(self, a:int, b:int):
        print("  !", a + b)

    def input_command(self):
        print("[%] Opened Debug Console")
        command = ""
        while command != "exit":
            command = input(" >> ")
            command = command.lstrip()
            
            if " " in command:
                command, parameters = command.split(" ", 1)
            else: parameters = ""

            if command not in self.command_list:
                print(f"[!] {command} is not a command")
                continue

            exec(self.command_list[command] + parameters + ")")


#debug_console = DebugConsole("")
#debug_console.input_command()