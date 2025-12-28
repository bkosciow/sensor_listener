
class Command:
    def __init__(self, patterns=None, command_with_text=False):
        self.patterns = patterns
        self.command = None
        self.command_with_text = command_with_text
        self.params = {}

    def parse(self, text):
        self.command = None
        self.params = {}
        if self.command_with_text:
            parts = text.split(' ', 1)
            if len(parts) < 2:
                return False
            self.command = parts[0]
            self.params['text'] = parts[1]

            return True

        if not self.patterns:
            return False
            
        for pattern in self.patterns:
            pattern_parts = pattern.split()
            text_parts = text.split()
            
            if len(pattern_parts) > 0 and len(text_parts) > 0 and len(pattern_parts) == len(text_parts):
                pattern_command = pattern_parts[0]
                text_command = text_parts[0]
                
                if pattern_command == text_command:
                    self.command = text_command
                    self.params = {}
                    
                    for i, pattern_part in enumerate(pattern_parts[1:], 1):
                        if i < len(text_parts):
                            param_name = pattern_part[1:-1]  # Remove < and >
                            self.params[param_name] = text_parts[i]
                    
                    return True
                
        return False

    def param(self, name):
        return self.params[name] if name in self.params else None

    def __getattr__(self, name):
        if name in self.params:
            return self.params[name]

        if name == 'command':
            return self.command

        if name == 'params':
            return self.params

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

if __name__ == '__main__':
    p = [
        '!sl <action>', '!sl <action> <module>'
    ]

    cmd = Command(p)
    cmd.parse("!sl data")
    assert "!sl" == cmd.command
    assert "data" == cmd.param("action")
    assert "data" == cmd.action
    
    cmd.parse("")
    assert None == cmd.command
    assert {} == cmd.params

    cmd.parse("!sl")
    assert None == cmd.command
    assert {} == cmd.params

    cmd.parse("!sl ")
    assert None == cmd.command
    assert {} == cmd.params

    cmd.parse("!sl air bb")
    assert "!sl" == cmd.command
    assert "air" == cmd.param("action")
    assert "air" == cmd.action
    assert "bb" == cmd.param("module")
    assert "bb" == cmd.module

    cmd = Command(command_with_text=True)
    cmd.parse("!question a long text following command")
    assert "!question" == cmd.command
    assert "a long text following command" == cmd.param("text")
    assert "a long text following command" == cmd.text

    cmd.parse("")

    cmd.parse("a")
    cmd.parse("a a")






