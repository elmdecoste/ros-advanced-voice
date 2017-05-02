class SpeechQueue():

    def __init__(self):
        self.commands = []
        self.length = 0

    def add(self, cmd):
        self.commands.append(cmd)
        self.length += 1

    def pop(self):
        self.length -= 1
        
        return temp

    def size(self):
        return self.length
