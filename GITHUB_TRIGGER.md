# GitHub Actions Deployment Trigger Guide

## Overview

You can trigger your GitHub Actions workflow using the `repository_dispatch` event. This allows you to programmatically start deployments from your Flask app.

## Setup Instructions

### 1. Create a GitHub Personal Access Token (PAT)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token and save it securely

### 2. Store Token as GitHub Secret (Recommended)

Instead of hardcoding the token, store it as an environment variable:

**Option A: GitHub Repository Secret**
1. Go to your repo: Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Name: `GITHUB_TOKEN_DISPATCH` (or `GITHUB_TOKEN`)
4. Value: Paste your PAT
5. Click "Add secret"

**Option B: Environment Variable (Local Development)**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
python app.py
```

### 3. Verify Workflow Configuration

Your `.github/workflows/deploy.yml` must have:

```yaml
on:
  repository_dispatch:
    types: [deploy_trigger]
```

✅ This is already configured in your workflow.

## Usage

### Method 1: Python Script (Direct)

```python
from github_trigger import trigger_deployment

# Trigger deployment
result = trigger_deployment(
    test_case="unit_tests",
    status="passed"
)

print(result)
# Output: {'success': True, 'message': "GitHub Action 'deploy_trigger' triggered successfully"}
```

### Method 2: Flask API Endpoint

**Start your Flask app:**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
python app.py
```

**Trigger via HTTP POST:**

```bash
curl -X POST http://localhost:5000/api/trigger-deploy \
  -H "Content-Type: application/json" \
  -d '{
    "test_case": "unit_tests",
    "status": "passed"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "GitHub Action 'deploy_trigger' triggered successfully"
}
```

### Method 3: With Custom Token (for CI/CD)

```bash
curl -X POST http://localhost:5000/api/trigger-deploy \
  -H "Content-Type: application/json" \
  -d '{
    "test_case": "integration_tests",
    "status": "passed",
    "token": "ghp_xxxxxxxxxxxx"
  }'
```

## Parameters

### Function Parameters

```python
trigger_github_action(
    owner="prakashdubey-solytics",        # Required: GitHub org/user
    repo="MemoApp",                        # Required: Repository name
    event_type="deploy_trigger",          # Optional: Event type (default: deploy_trigger)
    test_case="unit_tests",               # Optional: Test case name
    status="passed",                      # Optional: Test status
    payload={"custom": "data"},           # Optional: Additional data
    token="ghp_xxxx..."                   # Optional: GitHub token (uses env var if not provided)
)
```

### Payload in GitHub Actions

Your workflow receives this payload:

```json
{
  "client_payload": {
    "test_case": "unit_tests",
    "status": "passed",
    "service": "memo-app"
  }
}
```

Access in workflow:
```yaml
- name: Use payload
  run: |
    echo "Test Case: ${{ github.event.client_payload.test_case }}"
    echo "Status: ${{ github.event.client_payload.status }}"
```

## Workflow Trigger in deploy.yml

Example workflow that uses the payload:

```yaml
on:
  repository_dispatch:
    types: [deploy_trigger]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Get payload data
        run: |
          echo "Service: ${{ github.event.client_payload.service }}"
          echo "Test Case: ${{ github.event.client_payload.test_case }}"
          echo "Status: ${{ github.event.client_payload.status }}"
      
      - name: Trigger deployment
        if: github.event.client_payload.status == 'passed'
        run: echo "Deploying MemoApp..."
```

## Integration with Your App

### 1. Add to your index.html (Optional UI Button)

```html
<button onclick="triggerDeployment()">🚀 Trigger Deployment</button>

<script>
async function triggerDeployment() {
  const response = await fetch('/api/trigger-deploy', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      test_case: 'manual_trigger',
      status: 'initiated'
    })
  });
  
  const result = await response.json();
  alert(result.message);
}
</script>
```

### 2. Automated on Test Completion

```python
@app.route("/run-test")
def run_test():
    posts = Post.query.all()
    status = "passed" if len(posts) >= 0 else "failed"
    
    # Trigger deployment after test
    trigger_result = trigger_deployment(
        test_case="app_health_check",
        status=status
    )
    
    return jsonify({
        "test_status": status,
        "deployment_triggered": trigger_result.get("success")
    })
```

## Troubleshooting

### Error: "Unauthorized. Check your GitHub token"
- ❌ Token is invalid or expired
- ✅ Solution: Generate a new PAT and update GITHUB_TOKEN

### Error: "Repository not found"
- ❌ Incorrect owner/repo parameters
- ✅ Solution: Verify `prakashdubey-solytics/MemoApp` is correct

### Error: "Request timed out"
- ❌ GitHub API is slow or unreachable
- ✅ Solution: Retry in a few moments

### Workflow not triggering
- ❌ Repository dispatch event type mismatch
- ✅ Solution: Verify `.github/workflows/deploy.yml` has `types: [deploy_trigger]`

## Security Best Practices

✅ **DO:**
- Store token in GitHub Secrets
- Use environment variables
- Restrict token permissions (select scopes)
- Rotate tokens periodically

❌ **DON'T:**
- Commit token to repository
- Hardcode token in code
- Share token in chat/email
- Use tokens with excessive permissions

## Complete Example

```python
# app.py
from github_trigger import trigger_deployment

@app.route("/api/deploy", methods=["POST"])
def deploy():
    data = request.get_json()
    
    # Run tests first
    test_passed = run_tests()
    
    if test_passed:
        # Trigger GitHub Actions
        result = trigger_deployment(
            test_case="pre_deploy_tests",
            status="passed"
        )
        return jsonify({
            "tests": "passed",
            "deployment": result
        })
    else:
        return jsonify({"tests": "failed"}), 400
```

## API Reference

**Endpoint:** `POST /api/trigger-deploy`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "test_case": "string (optional)",
  "status": "string (optional)",
  "token": "string (optional - uses GITHUB_TOKEN env var if not provided)"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "GitHub Action 'deploy_trigger' triggered successfully"
}
```

**Error Response (400/401):**
```json
{
  "success": false,
  "message": "Error description",
  "status_code": 401
}
```
