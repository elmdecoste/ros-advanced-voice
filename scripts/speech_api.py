#!/usr/bin/env python

import rospy
from std_msgs.msg import String


class SpeechApi:
    def __init__(self):
        rospy.init_node('speech_api', anonymous=True)

        pub = rospy.Publisher('/autospeech/receive', String, queue_size=10)
        sub = rospy.Subscriber('/recognizer/output', String, self.received_speech)
        rate = rospy.Rate(10)  # 10hz

        self.currentText = ""

        while not rospy.is_shutdown():

            if len(self.currentText) > 0:
                rospy.loginfo(self.currentText)
                pub.publish(self.currentText)
                self.currentText = ""
            rate.sleep()

    def received_speech(self, data):
        rospy.loginfo("Received: " + data.data)
        self.currentText = data.data


if __name__ == '__main__':
    try:
        SpeechApi()
    except rospy.ROSInterruptException:
        pass
