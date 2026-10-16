# CampusDesk — DevOps Capstone

CampusDesk is a campus helpdesk for IT, facilities, and academic support. Students can raise requests, assign an owner, set a priority, and follow each ticket from open to resolved.

The application uses React, FastAPI, PostgreSQL, and Alembic. Its delivery stack includes Docker Compose, GitHub Actions, Trivy, GHCR, Terraform, Kubernetes, Helm, Prometheus, and Grafana.

## Run locally

Create `.env` from `.env.example` and choose a database password, then run:

```bash
docker compose up --build
```

Open `http://localhost:3000`. The backend API documentation is at `http://localhost:8000/docs`.

## Repository layout

- `backend/`: ticket API, database model, migrations, and tests.
- `frontend/`: responsive support dashboard and ticket actions.
- `helm/campusdesk/`: Kubernetes application chart.
- `terraform/`: VPC, two public subnets, and EKS worker group.
- `monitoring/`: Prometheus configuration and Grafana dashboard.
- `.github/workflows/`: test, build, scan, publish, and deploy pipeline.
- `evidence/`: recorded execution results and screenshots.

## API

`GET /health`, `GET /ready`, `GET /metrics`, `GET /api/tickets`, `GET /api/tickets/stats`, `GET /api/tickets/{id}`, `POST /api/tickets`, `PUT /api/tickets/{id}`, and `DELETE /api/tickets/{id}`.

This is a classroom application. It runs without user authentication and should be deployed only in a controlled demonstration environment.
