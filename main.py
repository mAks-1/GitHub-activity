import requests

def fetch_activity(username):
    url = f'https://api.github.com/users/{username}/events'

    try:
        response = requests.get(url)

        if response.status_code == 422:
            print("Validation error. Please check the username.")
            return None

        if response.status_code == 404:
            print(f"Error: Username '{username}' not found.")
            return None
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") 
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    if response.status_code == 422:
        print(f"Validation error: {response.json()}")

def parse_activity(events):
    """
    Parse the GitHub activity data and return a formatted list of activity descriptions.
    """
    activities = []
    for event in events:
        event_type = event['type']
        repo_name = event['repo']['name']

        if event_type == 'PushEvent':
            commit_count = event['payload']['size']
            activities.append(f"Pushed {commit_count} commit(s) to {repo_name}")
        elif event_type == 'CreateEvent':
            ref_type = event['payload']['ref_type']
            ref_name = event['payload']['ref'] if event['payload']['ref'] else 'repository'
            activities.append(f"Created a new {ref_type} {ref_name} in {repo_name}")
        elif event_type == 'IssuesEvent':
            action = event['payload']['action']
            issue_title = event['payload']['issue']['title']
            activities.append(f"{action.capitalize()} an issue '{issue_title}' in {repo_name}")
        elif event_type == 'WatchEvent':
            activities.append(f"Starred {repo_name}")
        else:
            activities.append(f"Performed {event_type} in {repo_name}")

    return activities

def main():
    """
    Main function to fetch and display GitHub activity.
    """
    print('You can check recent activity of a GitHub user\n')
    username = input('Enter username: ')
    events = fetch_activity(username)

    if not events:
        return 
    
    activities = parse_activity(events)

    print("\nRecent Activity:")
    for activity in activities:
        print(f"- {activity}")


if __name__ == "__main__":
    main()