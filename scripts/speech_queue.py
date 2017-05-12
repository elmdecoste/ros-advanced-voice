#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseGoal
from move_base_msgs.msg import MoveBaseAction
import re
from Command import Command
from Queue import Queue
import actionlib
from tf import transformations
from geometry_msgs.msg import Quaternion
from sound_play.libsoundplay import SoundClient
import genpy


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
            'turn': self.turn,
            'say': self.say
        }

        self.queue = Queue()
        self.sound_client = SoundClient()

        while not rospy.is_shutdown():
            if self.queue.not_empty:
                current = self.queue.get()

                if current.get_data_type() == SoundClient:
                    rospy.loginfo("Saying " + current.get_data())
                    self.sound_client.say(current.get_data())
                    rospy.sleep(2)
                else:
                    ac = actionlib.SimpleActionClient(current.get_path(), current.get_data_type())
                    ac.wait_for_server()

                    ac.send_goal_and_wait(current.get_data())

        rospy.spin()

    def received_command(self, data):
        split = re.split('///', data.data)
        command = self.typeSwitch[split[0]](split[1])
        self.queue.put(command)

    @staticmethod
    def navigate(location):
        goal = MoveBaseGoal()
        goal.target_pose.header.stamp = genpy.Time()
        goal.target_pose.header.frame_id = "/base_link"

        goal.target_pose.pose.position.x = 1.0
        goal.target_pose.pose.orientation.w = 1.0

        return Command('/move_base', MoveBaseAction, goal)

    @staticmethod
    def say(string):
        return Command('', SoundClient, string)

    @staticmethod
    def turn(direction):

        goal = MoveBaseGoal()
        goal.target_pose.header.stamp = genpy.Time()
        goal.target_pose.header.frame_id = "/base_link"

        dirs = {
            'left': 90,
            'right': -90
        }

        quaternion = transformations.quaternion_from_euler(0, 0, dirs[direction])

        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]

        return Command('/move_base', MoveBaseAction, goal)


if __name__ == '__main__':
    try:
        CommandScheduler()
    except rospy.ROSInterruptException:
        pass
