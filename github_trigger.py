"""
GitHub Actions Trigger Module

Safely trigger GitHub Actions using repository_dispatch events.
Token should be stored as environment variable or GitHub secret.
"""

import requests
import os
from typing import Dict, Any, Optional


def trigger_github_action(
    owner: str,
    repo: str,
    event_type: str = "deploy_trigger",
    test_case: Optional[str] = None,
    status: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Trigger a GitHub Action using repository_dispatch event.

    Args:
        owner: GitHub username/organization
        repo: Repository name
        event_type: Event type defined in workflow YAML (default: deploy_trigger)
        test_case: Test case name (optional)
        status: Test status (optional)
        payload: Additional payload data (dict) (optional)
        token: GitHub Personal Access Token (uses GITHUB_TOKEN env var if not provided)

    Returns:
        {
            "success": bool,
            "message": str,
            "status_code": int (if error)
        }

    Example:
        >>> result = trigger_github_action(
        ...     owner="prakashdubey-solytics",
        ...     repo="MemoApp",
        ...     test_case="unit_tests",
        ...     status="passed"
        ... )
        >>> print(result)
        {'success': True, 'message': 'GitHub Action triggered'}
    """

    # Get token from parameter or environment variable
    if not token:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            return {
                "success": False,
                "message": "GitHub token not provided. Set GITHUB_TOKEN env var or pass token parameter."
            }

    # Validate inputs
    if not owner or not repo:
        return {
            "success": False,
            "message": "owner and repo parameters are required"
        }

    # Build URL
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"

    # Build headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Build client payload
    client_payload = payload if isinstance(payload, dict) else {}
    
    # Add test_case and status if provided
    if test_case:
        client_payload["test_case"] = test_case
    if status:
        client_payload["status"] = status
    
    # Ensure service is set
    if "service" not in client_payload:
        client_payload["service"] = "memo-app"

    # Build request body
    data = {
        "event_type": event_type,
        "client_payload": client_payload
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)

        if response.status_code == 204:
            return {
                "success": True,
                "message": f"GitHub Action '{event_type}' triggered successfully"
            }
        elif response.status_code == 404:
            return {
                "success": False,
                "message": "Repository not found. Check owner and repo parameters.",
                "status_code": 404
            }
        elif response.status_code == 401:
            return {
                "success": False,
                "message": "Unauthorized. Check your GitHub token.",
                "status_code": 401
            }
        else:
            return {
                "success": False,
                "message": f"Failed to trigger GitHub Action",
                "status_code": response.status_code,
                "error": response.text
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "message": "Request timed out. GitHub API is not responding."
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Request failed: {str(e)}"
        }


# For use in your Flask app
def trigger_deployment(test_case: str, status: str) -> Dict[str, Any]:
    """
    Convenience function for triggering deployment in your MemoApp.
    
    Args:
        test_case: Name of the test case (e.g., "unit_tests", "integration_tests")
        status: Status of the test (e.g., "passed", "failed")
    
    Returns:
        Response dictionary with success status and message
    """
    return trigger_github_action(
        owner="prakashdubey-solytics",
        repo="MemoApp",
        event_type="deploy_trigger",
        test_case=test_case,
        status=status
    )


if __name__ == "__main__":
    # Example usage
    result = trigger_deployment(
        test_case="unit_tests",
        status="passed"
    )
    print(result)
