import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction
import re
from Command import Command
from Queue import Queue

class CommandScheduler:
    """
    Scheduler class for the multi-step speech processing
    """

    def __init__(self):
        rospy.init_node('command_scheduler', anonymous=True)

        self.rate = rospy.Rate(10)  # 10hz

        self.command_listener = rospy.Subscriber('/autospeech/run', String, self.received_command)

        self.typeSwitch = {
            'go': self.navigate,
            'say': self.say,
            'get': self.get
        }

        self.queue = Queue()

        while not rospy.is_shutdown():
            current = self.queue.get()
            rospy.Publisher(current.get_path(), current.get_data_type()).publish(current.get_data())

        rospy.spin()

    def received_command(self, data):
        split = re.split(data, '///')
        command = self.typeSwitch[split[0]](split[1])
        self.queue.put(command)

    def navigate(self, location):
        goal = MoveBaseAction()
        return Command('/move_base', MoveBaseAction, goal)

    def say(self, string):
        return Command('/sound_play', String, string)

    def get(self, obj):
        return Command('', obj)


if __name__ == '__main__':
    try:
        CommandScheduler()
    except rospy.ROSInterruptException:
        pass
