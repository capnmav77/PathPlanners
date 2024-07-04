# RclCPP = ros2 client library for c++

how to write a basic ros2 node : 
```
auto node = rclcpp::Node::make_shared("NodeName");
```
the above creates a shared pointer to ros2 node 

Geometry Messages : 
- they are messages that are used to define a agent's position and it's orientation , its a combination of it's dimensional position and it's orientation using quaternion.
- how to declare a geometry message :
  ```
    geometry_msgs::msg::Pose start_pose;
    start_pose.orientation.w = 1.0;
  ```

How to call other objects : 
- just like how you call normal objects :
  ```
      Agent_Robot agent(node, "agent_1", start_pose);
  ```
- here we call the agent_robot object and pass it the node , the agent name and the pose .


keep the node spinnin : rclcpp::spin(node);



# A ros Object for an agent : 
```cpp

// all the includes that are necessary to run the agent 
#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>  // for pose 
#include <tf2_ros/transform_broadcaster.h>  // for broadcasting the pose 

#include <visualization_msgs/msg/marker.hpp>  // for visualization marker that is used in rviz 
#include <geometry_msgs/msg/pose.hpp>  // for pose messages 
#include <geometry_msgs/msg/point.hpp>  // for point messages 

// include the types of messages that are passed to call a service 
#include <my_robot_interfaces/srv/update_goal.hpp>  
#include <my_robot_interfaces/srv/get_plan.hpp>
#include <my_robot_interfaces/msg/agent_info.hpp>

// some necessary libs 
#include <vector>

// making life easier
using namespace std::chrono_literals;
using namespace std::placeholders;
using std::vector;


class Agent_Robot 
{
public:
    explicit Agent_Robot(std::shared_ptr<rclcpp::Node> node, std::string serial_id, geometry_msgs::msg::Pose start_pose)
        : node_(node), serial_id(serial_id), pose(start_pose) // basically ban the compiler to convert the types from one to another to match the ctor .
    {

        int a = serial_id.at(6); // used to get the number from the agent -> agent_6 , 6 here
        srand(time(NULL) + a);
        // assign a random color to the agent 
        agent_color[0] = (rand() % 100) * 0.01;
        agent_color[1] = (rand() % 100) * 0.01;
        agent_color[2] = (rand() % 100) * 0.01;
        done = true;

        // creating a publisher for markers , agent and path that are visualized by rviz 
        pub_agent_marker_ = node_->create_publisher<visualization_msgs::msg::Marker>("/Rviz_marker_topic/base_link", 100);
        pub_path_marker_  = node_->create_publisher<visualization_msgs::msg::Marker>("/Rviz_marker_topic/path", 10);

        // creating a publisher for broadcasting the agent-info to all the subscribers .
        pub_agent_info_   = node_->create_publisher<my_robot_interfaces::msg::AgentInfo>("/agent_info", 100);

        // creating a service server that is used to update the agent's goal pose .
        service_ = node_->create_service<my_robot_interfaces::srv::UpdateGoal>("/update_goal", std::bind(&Agent_Robot::agent_update_goal,this,_1));

        // initializing a client for requesting a path plan 
        get_plan_service_client_ = node_->create_client<my_robot_interfaces::srv::GetPlan>("/get_plan");

        // transformBroadcaster for broadcasting transforms 
        br_ = std::make_unique<tf2_ros::TransformBroadcaster>(node_);

        // timer to update the agent's pose 
        timer_ = node_->create_wall_timer(std::chrono::duration<double>(1.0), std::bind(&Agent_Robot::agent_update_pose, this));
        RCLCPP_INFO(node_->get_logger(), "Ready to update goal pose for agent");
    }

private:

    std::shared_ptr<rclcpp::Node> node_; // shared pointer to the ros2 node .
    std::string serial_id; // unique id for the agent             
    geometry_msgs::msg::Pose pose; // current pose 

    // declaration of all the shared pointers for 
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr pub_agent_marker_;
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr pub_path_marker_;
    rclcpp::Publisher<my_robot_interfaces::msg::AgentInfo>::SharedPtr pub_agent_info_;  
    rclcpp::Client<my_robot_interfaces::srv::GetPlan>::SharedPtr get_plan_service_client_;                    
    rclcpp::Service<my_robot_interfaces::srv::UpdateGoal>::SharedPtr service_;

    rclcpp::TimerBase::SharedPtr timer_;
    std::unique_ptr<tf2_ros::TransformBroadcaster> br_;

    double agent_color[3];                                 
    bool done;   // flag indicating if the agent has reached it's goal                                           
    geometry_msgs::msg::Pose goal_pose;     // desired pose for the agent               
    vector<geometry_msgs::msg::Point> point_list;          // list of points defining a path for the agent 


// helper functions / Member functions :

    // a function to update the agent's pose based on the pre-defined path and publishes agent information and markers 
    void agent_update_pose()
    {   
        static int index =0;

        if (!done)
        {   
            pose.position.x = point_list.at(index).x;
            pose.position.y = point_list.at(index).y;
            index++;

            if (index == int(point_list.size()))
            {
                done = true;
                index = 0;
                RCLCPP_INFO(node_->get_logger(),"Target goal has been reached by %s", serial_id.c_str());
            }

        }

        my_robot_interfaces::msg::AgentInfo msg;  // a message for publishing the agent info 
        msg.serial_id = serial_id;
        msg.pose = pose;
        pub_agent_info_->publish(msg); // publishing the agent's information onto the /agent_info topic .
        agent_update_transform(pose); // converts the agent's pose into a transform message and broadcasts it 
        agent_build_agent_marker();  // constructs and publishes a marker representing the agent 
    }


    // service callback function that updates the agent's goal pose and requests a path plan
    void agent_update_goal(std::shared_ptr<my_robot_interfaces::srv::UpdateGoal::Request> req)
    {
        goal_pose = req->goal_pose;
        RCLCPP_INFO(node_->get_logger(),"Intiating Movement to (%f,%f)", goal_pose.position.x,goal_pose.position.y);
        
        auto request =std::make_shared<my_robot_interfaces::srv::GetPlan::Request>();
        request->serial_id=serial_id;
        request->goal_pose=goal_pose;

        auto result= get_plan_service_client_->async_send_request(request,std::bind(&Agent_Robot::responesCallback, this,_1));

    }


    // callback function invoked when a path plan is received , updates the point_list and triggers path visualization using agent_build_path_marker and the current path
    void responesCallback(rclcpp::Client<my_robot_interfaces::srv::GetPlan>::SharedFuture future)
    {
        if(future.valid())
        {
            point_list=future.get()->path;

            done = false;
            RCLCPP_INFO(node_->get_logger(), "Path Returned");
            agent_build_path_marker(future.get()->path); 
        }
        
    }

    // converts the agent pose into a transform message and broadcasts it 
    void agent_update_transform(geometry_msgs::msg::Pose pose)
    {   
        geometry_msgs::msg::TransformStamped transform;
        tf2::Quaternion q;

        q.setX(pose.orientation.x);
        q.setY(pose.orientation.y);
        q.setZ(pose.orientation.z);
        q.setW(pose.orientation.w);
        q.normalize();

        transform.header.stamp = node_->now();
        transform.header.frame_id = "world";
        transform.child_frame_id = serial_id;
        transform.transform.translation.x = pose.position.x;
        transform.transform.translation.y = pose.position.y;
        transform.transform.rotation.x = q.x();
        transform.transform.rotation.y = q.y();
        transform.transform.rotation.z = q.z();
        transform.transform.rotation.w = q.w();
        br_->sendTransform(transform);
    }


    // constructs and publishes a marker representing the agent 
    void agent_build_agent_marker()
    {
        visualization_msgs::msg::Marker marker;
        marker.header.frame_id = serial_id;
        marker.header.stamp = node_->now();
        marker.ns = serial_id;
        marker.id = 1;
        marker.type = visualization_msgs::msg::Marker::CUBE;
        marker.action = visualization_msgs::msg::Marker::ADD;
        marker.pose.position.z = 0.25;
        marker.scale.x = 1.0;
        marker.scale.y = 1.0;
        marker.scale.z = 0.5;
        marker.color.a = 1.0;
        marker.color.r = agent_color[0];
        marker.color.g = agent_color[1];
        marker.color.b = agent_color[2];
        pub_agent_marker_->publish(marker);
    }


    // constructs and publishes a marker representing the path followed by the agent
    void agent_build_path_marker(vector<geometry_msgs::msg::Point> vect)
    {
        visualization_msgs::msg::Marker marker;
        marker.header.frame_id = "world";
        marker.header.stamp = node_->now();
        marker.ns = serial_id;
        marker.id = 0;
        marker.type = visualization_msgs::msg::Marker::LINE_STRIP;
        marker.action = visualization_msgs::msg::Marker::ADD;
        marker.pose.orientation.w = 1.0;
        marker.scale.x = 0.05;
        marker.color.r = agent_color[0];
        marker.color.g = agent_color[1];
        marker.color.b = agent_color[2];
        marker.color.a = 1.0;
        marker.points = vect;
        pub_path_marker_->publish(marker);
    }

};
```

