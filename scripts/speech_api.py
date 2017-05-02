
#BWI_Tasks visid_list_gui.cpp

import rospy
from std_msgs.msg import String

def speech_api():
    pub = rospy.Publisher('/autospeech/receive', String, queue_size=10)
    rospy.init_node('speech_api', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        hello_str = "go to this location and get some stuff"
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        speech_api()
    except rospy.ROSInterruptException:
        pass
        