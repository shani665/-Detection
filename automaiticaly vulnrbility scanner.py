import requests

# Coverity server details
COVERITY_URL = "https://coverity-server.example.com"
API_TOKEN = "your_coverity_api_token"

# API endpoints
PROJECTS_ENDPOINT = f"{COVERITY_URL}/api/v2/projects"
ISSUES_ENDPOINT = f"{COVERITY_URL}/api/v2/issues"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_projects():
    """Fetch the list of projects from Coverity."""
    response = requests.get(PROJECTS_ENDPOINT, headers=HEADERS, verify=False)
    if response.status_code == 200:
        projects = response.json()["projects"]
        return [(proj["id"], proj["name"]) for proj in projects]
    else:
        print(f"Error fetching projects: {response.status_code}")
        return []

def get_vulnerabilities(project_id):
    """Fetch vulnerabilities for a given project."""
    params = {"projectId": project_id, "status": "Open"}
    response = requests.get(ISSUES_ENDPOINT, headers=HEADERS, params=params, verify=False)
    if response.status_code == 200:
        issues = response.json()["issues"]
        return issues
    else:
        print(f"Error fetching vulnerabilities: {response.status_code}")
        return []

def main():
    """Main function to detect and report vulnerabilities."""
    print("Fetching projects...")
    projects = get_projects()
    if not projects:
        print("No projects found.")
        return

    for project_id, project_name in projects:
        print(f"\nAnalyzing project: {project_name} (ID: {project_id})")
        vulnerabilities = get_vulnerabilities(project_id)
        if vulnerabilities:
            print(f"Found {len(vulnerabilities)} open vulnerabilities:")
            for issue in vulnerabilities:
                print(f"  - ID: {issue['id']}, Severity: {issue['severity']}, "
                      f"Type: {issue['issueKind']}, Description: {issue['description']}")
        else:
            print("No open vulnerabilities found.")

if __name__ == "__main__":
    main()
