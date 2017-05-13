#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Bool
import re

available_commands = [
    ("go", "\\bforwards?\\b|\\bbackwards?\\b"),
    ("turn", "\\bleft\\b|\\bright\\b"),
    ("say", "^say\s*(.*)")
]

available_separators = "\\band\\b|\\bthen\\b"


class CommandProcessor:
    """
    ROS Processor class
    """

    def __init__(self, separators, commands):
        rospy.init_node('command_processor', anonymous=True)

        self.command = ""
        self.rate = rospy.Rate(10)  # 10hz
        self.separator_regex = separators
        self.commands = commands
        self.separator = '///'

        self.speech_listener = rospy.Subscriber('/autospeech/receive', String, self.received_command)

        self.cmd_publisher = rospy.Publisher('/autospeech/run', String, queue_size=10)

        rospy.spin()

    def received_command(self, data):
        """
        :param data: string command to parse
        """
        self.command = data.data

        lowered = self.command.lower()
        self.split = re.split(self.separator_regex, lowered)
        rospy.loginfo(lowered)
        for cmd in self.split:
            self.process(cmd.strip())
        print "\n"

    def process(self, cmd):
        for available_cmd in self.commands:
            if cmd.find(available_cmd[0]) != -1:
                command = available_cmd[0]
                params = re.findall(available_cmd[1], cmd)

                if not len(params) > 0:
                    rospy.logerr("Command not processed")
                    break

                rospy.loginfo("Command: " + available_cmd[0])
                rospy.loginfo("Parameters: %s" % params[0])

                self.cmd_publisher.publish(command + self.separator + params[0])
                break


if __name__ == "__main__":
    try:
        processor = CommandProcessor(available_separators, available_commands)
    except rospy.ROSInterruptException:
        pass
