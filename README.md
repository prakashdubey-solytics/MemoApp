# Flask CRUD Application

A modern, production-ready Flask application with complete CRUD operations, local SQLite database, and Kubernetes deployment support.

## Features

✅ **Full CRUD Operations**
- Create, Read, Update, Delete posts
- Search functionality
- Timestamps for every post

✅ **Database**
- Local SQLite database
- SQLAlchemy ORM
- Automatic migrations

✅ **REST API**
- JSON endpoints for programmatic access
- GET, POST, PUT, DELETE support

✅ **Modern UI**
- Responsive design
- Beautiful gradient theme
- Intuitive user experience

✅ **Production Ready**
- Docker containerization
- Kubernetes manifests
- GitHub Actions CI/CD
- Health checks
- Resource limits

## Quick Start

### Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Visit http://localhost:5000

### Docker

```bash
docker-compose up -d
```

## Project Structure

```
flask-app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local development setup
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker build ignore
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── k8s/                        # Kubernetes manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── kustomization.yaml
├── templates/
│   ├── index.html              # Main page
│   └── edit.html               # Edit page
└── README.md                   # This file

```

## API Endpoints

### Web Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | List all posts |
| `/create` | POST | Create new post |
| `/edit/<id>` | GET/POST | Edit post |
| `/delete/<id>` | POST | Delete post |

### API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/api/posts` | GET | Get all posts (JSON) |
| `/api/posts/<id>` | GET | Get single post (JSON) |
| `/api/posts` | POST | Create post (JSON) |
| `/api/posts/<id>` | PUT | Update post (JSON) |
| `/api/posts/<id>` | DELETE | Delete post (JSON) |

## Deployment

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

### Quick Kubernetes Deploy

```bash
kubectl apply -k k8s/
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| FLASK_ENV | production | Flask environment |
| FLASK_DEBUG | false | Debug mode |
| DATABASE_URL | sqlite:///posts.db | Database connection |

## Tech Stack

- **Backend**: Flask 3.0.0
- **Database**: SQLite + SQLAlchemy
- **Server**: Gunicorn
- **Container**: Docker
- **Orchestration**: Kubernetes
- **CI/CD**: GitHub Actions

## Development

### Install dev dependencies

```bash
pip install pytest pytest-cov flake8
```

### Run tests

```bash
pytest
```

### Lint code

```bash
flake8 .
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/Amazing`)
3. Commit changes (`git commit -m 'Add Amazing feature'`)
4. Push to branch (`git push origin feature/Amazing`)
5. Open Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.

---

Made with ❤️ for production-ready Flask apps
