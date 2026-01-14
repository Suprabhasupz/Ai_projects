#!/usr/bin/env python3

# license removed for brevity

import rospy
import actionlib
import time
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
n = input("user input")
needed_delay = input("enter delay")
def movebase_client():
    
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x= -1.58
    goal.target_pose.pose.position.y = -0.452
    goal.target_pose.pose.orientation.w = 0.00247
    time.sleep(needed_delay)
    client.send_goal(goal)
    
    wait = client.wait_for_result()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1.48
    goal.target_pose.pose.position.y =  -0.605
    goal.target_pose.pose.orientation.w = 0.00247
    time.sleep(needed_delay)
    client.send_goal(goal)
    
    wait = client.wait_for_result()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = 1.64
    goal.target_pose.pose.position.y = 0.686
    goal.target_pose.pose.orientation.w = 0.0025
    time.sleep(needed_delay)
    client.send_goal(goal)
    
    wait = client.wait_for_result()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = -1.68
    goal.target_pose.pose.position.y = 0.597
    goal.target_pose.pose.orientation.w = 0.0025
    time.sleep(needed_delay)
    client.send_goal(goal)
    
    wait = client.wait_for_result()
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = -1.58
    goal.target_pose.pose.position.y = -0.452
    goal.target_pose.pose.orientation.w = 0.00247
    time.sleep(needed_delay)
    
    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()


if __name__ == '__main__':
    try:
      while (n>0):
        
         rospy.init_node('movebase_client_py')
         result = movebase_client()
         
         if result:
             print (n)
             n = n - 1
             rospy.loginfo("Goal execution done!")
            
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

        pass
