## How to setup the Ros2 action client . 
- copy the action client file from here onto your package 
``` py
import rclpy
from rclpy.node import Node
from arduinobot_msgs.action import Fibonacci


class SimpleActionClient(Node):

    def __init__(self):
        super().__init__('action_client') # initialize the node with the name 'action_client'
        self.action_client = ActionClient(self, "fibonacci") # create an action client for the Fibonacci action
        
        self.action_client.wait_for_server() # wait for the action server to be up

        self.goal = Fibonacci.Goal() # create a goal message for the Fibonacci action 
        self.goal.order = 10 # set the order of the Fibonacci sequence to 10 where order is a field in the Fibonacci action goal message
        self.future = self.action_client.send_goal_async(self.goal, feedback_callback=self.feedbackCallback) # send the goal to the action server and specify the feedback callback
        self.future.add_done_callback(self.responseCallback) # specify the response callback


    def responseCallback(self, future):
        goal_handle = future.result()
        # if the goal is rejected
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        # if the goal is accepted
        self.get_logger().info('Goal accepted :)')

        # since it's accepted and the goal is to calculate the Fibonacci sequence, we wait for the result
        self.get_logger().info('Waiting for result...')
        self.future = goal_handle.get_result_async() # get the result of the goal asynchronously and store it in self.future

        self.future.add_done_callback(self.resultCallback)
    

    def resultCallback(self, future):
        result = future.result().result
        self.get_logger().info("Result: {0}".format(result.sequence)) # print the result of the Fibonacci sequence
        rclpy.shutdown()


    def feedbackCallback(self, feedback_msg):
        self.get_logger().info('Feedback received: {0}'.format(feedback_msg.feedback.partial_sequence))



def main(args=None):
    rclpy.init(args=args) # initialize the ROS client library
    action_client = SimpleActionClient() # create an instance of the SimpleActionClient class
    rclpy.spin(action_client) # keep the node running 
     
```

- on the setup.py file add the following into console scripts : 
``` py
'simple_action_client = YourFolderName.Action_client:main'
```

- then use the below on your ros2 workspace : 
``` bash
colcon build 
```
 
- create a new workspace run the server and then use the below in a new terminal : 
``` 
. install/setup.bash
ros2 run yourpackagename simple_action_client 
```