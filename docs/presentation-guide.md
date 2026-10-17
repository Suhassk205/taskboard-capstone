# CampusDesk presentation guide

CampusDesk handles campus support requests across IT, facilities, and academics. The application domain is a helpdesk: the central record is a ticket with a requester, category, priority, owner, and status.

## Demonstration order

1. Open `http://localhost:3000`. Create a request, assign it, move it to In progress, resolve it, edit it, and delete a demonstration record. Explain how the request counters change.
2. Open `http://localhost:8000/docs` and show the GET, POST, PUT, and DELETE operations. Explain that `/health` checks liveness while `/ready` also verifies PostgreSQL access.
3. Show the database migration and the `tickets` table. Alembic tracks schema versions; the advisory lock prevents two starting replicas from migrating simultaneously.
4. Run `pytest -v` in `backend/`. The fixture creates a new SQLite database for every test, so test data cannot affect the running PostgreSQL database.
5. Show the Dockerfiles and Compose stack. Explain the frontend's Node build stage, smaller Nginx runtime, and non-root users. Show the healthy containers.
6. Show a small application change, its commit, and the GitHub Actions run. Tests and the frontend build finish before image publication. A failed test stops the release.
7. Open both Trivy steps. Explain the HIGH/CRITICAL gate and the recorded clean result. Show the backend and frontend packages in GHCR and their full Git SHA tags.
8. Show the Terraform files and recorded AWS Console views. Describe the VPC, two public subnets, Internet Gateway, EKS control plane, and managed worker group. Show the completed destroy transcript and empty final state.
9. Show `kubectl get pods,svc,ingress,hpa -n campusdesk` and `helm list -n campusdesk`. Explain Deployments, stable Service addresses, the PostgreSQL PVC, and release revisions.
10. Open `http://campusdesk.localhost:8088`. Explain how Ingress sends `/api` to FastAPI and `/` to the frontend. The two frontend replicas and at least two backend replicas are separate from PostgreSQL's single replica.
11. Show the HPA transcript: real API traffic raised backend CPU and the HPA increased replicas from two to four. CPU requests are the denominator for the utilization target; Metrics Server supplies the measurements.
12. Open Prometheus Targets and the Grafana dashboard. Prometheus scrapes each Running backend Pod; Grafana plots those collected request counters and rates.
13. Show the isolated troubleshooting transcript. A wrong image tag prevented startup; a wrong Service selector produced no endpoints. Fixing the image and labels restored the workload and connectivity.

## Recorded release

The delivery recording follows one real frontend change through a pushed commit, hosted tests, image builds, Trivy, GHCR publication, and deployment. The laptop pulls the exact published images and upgrades its Helm release; the updated description and embedded Git SHA are checked in the deployed frontend asset.

The GitHub runner's cluster is temporary and removed at the end of its job. The laptop's Kind cluster remains available for the presentation. AWS infrastructure was created for the Terraform exercise and destroyed after evidence collection.

## Useful commands

```bash
docker compose ps
docker compose exec postgres psql -U campusdesk -d campusdesk -c 'SELECT * FROM alembic_version;'
docker compose exec postgres psql -U campusdesk -d campusdesk -c 'SELECT id,title,status,priority FROM tickets;'
kubectl -n campusdesk get pods,svc,ingress,hpa
helm list -n campusdesk
helm history campusdesk -n campusdesk
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8001/metrics
```

## Decisions to explain

- React and FastAPI communicate through relative `/api` routes, so the browser does not need internal Kubernetes hostnames.
- Readiness prevents traffic reaching a backend that cannot access the database; liveness detects a failed application process.
- SHA tags link an image to the source commit that produced it and make upgrades and rollbacks traceable.
- Container scanning is one security control. It does not replace authentication, secret management, or runtime monitoring.
- The AWS exercise uses public worker subnets to keep the classroom lab small. Private workers and managed database services would be separate production design decisions.
- PostgreSQL uses persistent storage in the local cluster. Running two API replicas does not make the database highly available.
