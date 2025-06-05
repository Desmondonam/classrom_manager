import requests
from django.conf import settings

class GitHubClassroomService:
    def __init__(self):
        self.token = settings.GITHUB_TOKEN
        self.org = settings.GITHUB_ORG
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_assignment_repos(self, assignment_prefix):
        """Get all repositories for a specific assignment"""
        if not self.token:
            return []
        
        url = f'https://api.github.com/orgs/{self.org}/repos'
        try:
            response = requests.get(url, headers=self.headers)
            repos = response.json()
            return [repo for repo in repos if repo['name'].startswith(assignment_prefix)]
        except Exception as e:
            print(f"Error fetching repos: {e}")
            return []
    
    def check_repo_exists(self, repo_name):
        """Check if a repository exists"""
        if not self.token:
            return False
        
        url = f'https://api.github.com/repos/{self.org}/{repo_name}'
        try:
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except Exception as e:
            print(f"Error checking repo: {e}")
            return False