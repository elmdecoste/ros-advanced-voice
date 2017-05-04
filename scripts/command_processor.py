import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool

import re

available_commands = [
    ("go", "^go\s*(\\bto\\b|\\bthrough\\b|\\bget\\b)\\s*(.*)$", 2),
    ("get", "^get\\s(.*)$", 1),
    ("say", "^say\\s(.*)$", 1)
]

# Lights => segbot_led
# Turn =>
# Move =>
# Navigation =>
# Say => sound_play

available_separators = "and|then"


class CommandProcessor:
    """
    ROS Processor class
    """

    def __init__(self, separators, commands):
        rospy.init_node('command_processor', anonymous=True)

        self.command = ""
        self.status = False
        self.rate = rospy.Rate(10)  # 10hz
        self.separator_regex = separators
        self.commands = commands
        self.separator = '///'

        self.speech_listener = rospy.Subscriber('/autospeech/receive', String, self.received_command)

        self.status_listener = rospy.Subscriber('/autospeech/status', Bool, self.update_status)

        self.cmd_publisher = rospy.Publisher('/autospeech/run', String, queue_size=10)

        rospy.spin()

    def received_command(self, data):
        """
        :param data: string command to parse
        """
        self.command = data.data

        lowered = self.command.lower()
        self.split = re.split(self.separator_regex, lowered)

        for cmd in self.split:
            self.process(cmd.strip())
        print "\n"

    def process(self, cmd):
        for available_cmd in self.commands:
            if cmd.find(available_cmd[0]) != -1:
                command = available_cmd[0]
                params = re.split(available_cmd[1], cmd)[available_cmd[2]]

                print "Command: " + available_cmd[0]
                print "Parameters: %s" % params

                self.cmd_publisher.publish(command + self.separator + params)

    def update_status(self, data):
        """
        :param data: boolean on if the scheduler will accept a new dataset
        """
        self.status = data.data


if __name__ == "__main__":
    try:
        processor = CommandProcessor(available_separators, available_commands)
    except rospy.ROSInterruptException:
        pass
