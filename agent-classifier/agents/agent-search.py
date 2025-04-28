import json
import os

def load_manifest(manifest_path, agent_name):
    with open(manifest_path, 'r') as file:
        # Parse the manifest file once
        manifest_records = json.load(file)
        # print(f"Manifest records: {manifest_records}")
        # Strip @ symbol from agent_name if present
        search_name = agent_name.lstrip('@') if agent_name and agent_name.startswith('@') else agent_name
        
        agents = manifest_records.get('agents', [])

        # Search for the agent in the manifest
        for agent in agents:
            if agent['agent-name'] == search_name:
                return agent['agent_id']
        return None

def main():
    # Example usage
    manifest_path = 'agents-manifest.json'
    agent_name = '@weather'
    agent_id = load_manifest(manifest_path, agent_name)
    print(f"Agent ID: {agent_id}")

if __name__ == "__main__":
    main()