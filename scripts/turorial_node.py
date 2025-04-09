#!/usr/bin/env python
import rospy

def main():
    rospy.init_node('hello_world_node')

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        rospy.loginfo("Hello, world!")
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass