# Capstone requirements

| Module | Required evidence |
|---|---|
| M1 | Browser application, CRUD endpoints, PostgreSQL table and Alembic migration |
| M2 | At least five passing tests covering three endpoints, isolated test database |
| M3 | Public repository, meaningful history with at least ten commits, ignored secrets and dependencies |
| M4 | Non-root backend and multi-stage frontend images; complete Compose stack |
| M5 | Hosted tests, frontend build, two images in GHCR with commit-SHA tags |
| M6 | Trivy scan of both images; HIGH/CRITICAL failure gate and explanation |
| M7 | Valid Terraform, real VPC/two public subnets/EKS worker group, AWS Console and destroy evidence |
| M8 | Namespace, Helm release, two replicas of each application, Services, working Ingress |
| M9 | Backend metrics, Prometheus target UP, populated Grafana application panel |
| M10 | Root README and a live or recorded commit-to-deployment walkthrough |

The final demonstration also includes autoscaling and troubleshooting broken images and Service selectors. Execution evidence is recorded after running the corresponding commands.
