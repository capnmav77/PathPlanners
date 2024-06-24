class Collision_Manager:
    def detect_collision(self, Agent , agents):
        for agent in agents:
            if agent != Agent and agent.get_current_coordinates() == Agent.get_next_coordinates():
                print("Collision detected between agent ", Agent.get_agent_id(), " and agent ", agent.get_agent_id())
                return True
        return False