import os
import sys

# Manual .env file loading
def load_env_file():
    try:
        with open('/Users/bard/Code/Ollama_Experiments/.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
    except Exception as e:
        print(f"Note: Could not load .env file: {e}")

# Load environment variables
load_env_file()

# Set default Ollama configuration if not provided in .env
if "OLLAMA_HOST" not in os.environ:
    os.environ["OLLAMA_HOST"] = "http://localhost:11434"
if "OLLAMA_MODEL" not in os.environ:
    os.environ["OLLAMA_MODEL"] = "deepseek-r1"

# Simulated AgentAPI for demonstration
class AgentAPI:
    """Simplified AgentAPI implementation for demonstration"""
    
    @staticmethod
    def list_agents():
        """Return all available agent types"""
        return {
            "chat": "General conversational agent",
            "debug": "Specialized for debugging code",
            "research": "Specialized for research tasks",
            "memory": "Agent with enhanced memory capabilities"
        }
    
    @staticmethod
    def create_session(agent_type, config=None):
        """Create a new agent session"""
        if agent_type not in AgentAPI.list_agents():
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # In a real implementation, we would connect to Ollama here
        # For demo purposes, we just return a simple session ID
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def get_response(session_id, user_input):
        """Process user input and return agent response"""
        import requests
        
        # Connect to Ollama API
        try:
            response = requests.post(
                f"{os.environ['OLLAMA_HOST']}/api/generate",
                json={
                    "model": os.environ["OLLAMA_MODEL"],
                    "prompt": user_input,
                    "stream": False
                }
            )
            response.raise_for_status()
            result = response.json()
            return {
                "reply": result.get("response", "Sorry, I couldn't generate a response."),
                "session_id": session_id
            }
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            return {
                "reply": "I'm having trouble connecting to my language model backend.",
                "session_id": session_id,
                "error": str(e)
            }
    
    @staticmethod
    def terminate_session(session_id):
        """End an agent session"""
        # In a real implementation, we would clean up resources
        return True

def main():
    print("Simple Ollama Agent Chat Demo")
    print("===========================")
    
    # List available agents
    agents = AgentAPI.list_agents()
    print("Available agents:")
    for agent_type, description in agents.items():
        print(f"- {agent_type}: {description}")
    
    # Use the chat agent for demonstration
    agent_type = "chat"
    print(f"\nUsing {agent_type} agent for demonstration")
    
    # Create a session
    try:
        session_id = AgentAPI.create_session(agent_type)
        print(f"Created {agent_type} agent session: {session_id}")
        
        # Demo conversation with predefined messages
        demo_messages = [
            "Hello! Can you introduce yourself?",
            "What can you help me with?",
            "Tell me a short joke"
        ]
        
        for user_input in demo_messages:
            print(f"\nYou: {user_input}")
            
            # Get response
            response = AgentAPI.get_response(session_id, user_input)
            print(f"Agent: {response['reply']}")
        
        # Clean up
        AgentAPI.terminate_session(session_id)
        print("\nDemo completed. Session terminated.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()