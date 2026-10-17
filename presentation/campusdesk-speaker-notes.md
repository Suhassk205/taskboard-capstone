# CampusDesk presentation speaker notes

Suggested length: 12 to 15 minutes, plus the optional delivery recording.

## 01 CampusDesk

CampusDesk is a campus helpdesk. The application lets students raise requests for IT, facilities, and academics, and lets a support team assign ownership and track progress. This presentation follows the application through tests, containers, automated delivery, infrastructure, Kubernetes, and monitoring. The screenshots and logs come from the project repository. The AWS exercise provisioned real infrastructure and removed it after verification. The application demonstration runs on the laptop and on temporary CI clusters.

Sources:
- https://github.com/Suhassk205/taskboard-capstone

## 02 Campus support requests

The central record is a support ticket. It stores a title, description, requester, category, owner, priority, and status. The dashboard reads live API data and shows request counts. For the application demo, create a sample request, assign it, change its status, and show the counters updating. The seeded workspace contains eight sample requests. These are demonstration records. Loading and error states also appear when the API is unavailable. The frontend has responsive layouts for smaller screens.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/04-api-database.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/10-compose-application.png

## 03 Application architecture

The browser runs React. Nginx serves the built frontend and handles relative API requests in Compose. In Kubernetes, the Ingress controller routes the browser request to the appropriate Service. FastAPI validates requests and uses SQLAlchemy to access PostgreSQL. Alembic controls schema changes. Helm packages the Kubernetes resources. Prometheus collects backend metrics, and Grafana displays them. Application workloads run on Kind locally and in CI. Terraform provisions a separate AWS VPC and EKS exercise, which was destroyed after verification.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/README.md
- https://github.com/Suhassk205/taskboard-capstone/blob/main/docker-compose.yml

## 04 REST API and PostgreSQL

The API implements the required GET, POST, PUT, and DELETE operations. Additional routes provide ticket statistics, readiness, liveness, and metrics. Alembic migration 0001 creates the tickets table in PostgreSQL. At startup, the backend takes a PostgreSQL advisory lock before running migrations. That serializes schema updates when multiple replicas start together. The recorded CRUD exercise created, read, updated, and deleted a ticket, then inspected the PostgreSQL table and Alembic version. Explain that /ready verifies database connectivity, while /health checks application liveness.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/04-api-database.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/backend/app/main.py

## 05 Automated API tests

The backend test suite has sixteen passing cases. Tests cover health, readiness, creation, reading, listing, updates, deletion, statistics, filtering, search, validation, missing records, metrics, and an empty workspace. The fixture replaces the application database dependency with a fresh SQLite database for each case. Tests never use the running PostgreSQL database. Pytest runs before image building and publication in GitHub Actions, so a failing test stops the release. Show the passing output and identify the fixture in backend/tests/conftest.py.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/02-backend-tests.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/11-pytest-results.png

## 06 Git history and traceability

The initial publication snapshot contains eleven commits: repository initialization and ten meaningful implementation commits. Each implementation commit describes a concrete part of the project, including the database, API, tests, frontend, containers, Helm, infrastructure, or pipeline. Later commits add verification evidence and presentation materials. The full history remains available in the public repository. The ignore rules exclude environment files, virtual environments, node_modules, caches, Terraform state, local inputs, and saved plans. The security audit checked both history and staged publication for secrets.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/01-published-commit-history.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/01-published-commit-history.png

## 07 Docker and Compose

Docker Compose runs the entire local stack with one command. PostgreSQL uses a named volume, so its data survives a normal Compose shutdown. Health checks control startup order. The backend image installs Python dependencies and runs migrations before Uvicorn starts. The frontend has a Node build stage and an Nginx runtime stage, so the final image does not contain the frontend build toolchain. Both application containers run as non-root users. The evidence records all services, readiness checks, HTTP responses, and the actual user IDs.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/03-compose-stack.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/12-compose-stack.png

## 08 CI/CD on every push

Every push to main triggers the GitHub Actions workflow. The test job runs pytest and builds the React frontend. The next job builds the backend and frontend images and scans each one. Publication happens only after the security gates pass. The deploy job pulls the published images into a temporary Kind cluster, installs the Helm chart, waits for healthy workloads, and checks /ready. The runner removes its temporary cluster at the end. This is a real hosted deployment check, and the laptop demonstration also installs the exact published images.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/15-hosted-run.json
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/14-ci-success.png

## 09 Container security gates

Trivy scans both application images for vulnerabilities in installed operating-system packages and application dependencies. The workflow sets HIGH and CRITICAL as the blocking severities, with exit code one on a finding. The recorded release returned zero findings at those severities for both images. A clean scan describes those image contents and the vulnerability database at scan time. It does not prove that the application has authentication or that later databases will remain clean. Explain the difference between container vulnerability scanning and the separate secret check on Git history.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/16-trivy-backend.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/17-trivy-frontend.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/.github/workflows/ci-cd.yml

## 10 Published images in GHCR

The registry contains separate backend and frontend packages. Each published image uses the full Git commit SHA as its tag. That gives a direct connection between source, workflow run, image, and deployment. The package screenshot shows real published SHA tags. For the recorded release, the laptop pulled both exact images from GHCR instead of rebuilding a different local artifact. The deployment transcript contains the pull output, image digests, loaded images, and Kubernetes image references. Open the package page and compare an image tag with its source commit.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/18-recorded-delivery.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/18-ghcr-frontend.png

## 11 Terraform on AWS

Terraform initialized, validated the HCL, and produced a non-empty plan before provisioning. It created fifteen managed resources in ap-south-1. The VPC has two public subnets in separate availability zones, an Internet Gateway, routing, and the IAM roles required by EKS. The exercise uses public worker subnets to keep the classroom setup small. It does not add a NAT Gateway or a managed database. These Console screenshots are historical evidence from the verified provisioning run. The infrastructure was removed after the screenshots and status checks.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/07-terraform-plan.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/21-aws-vpc-console.png

## 12 EKS and managed workers

The Terraform exercise created a real EKS control plane and a managed worker group with two t3.small nodes. AWS reported both resources as ACTIVE, and the worker nodes reached Ready. The Console view shows the cluster in the Mumbai region. This validates the infrastructure module. Application workloads and the monitoring demonstration run on Kind locally and in CI, which is separate from this AWS provisioning exercise. All AWS resources from the exercise were destroyed after verification. Do not describe this screenshot as a currently running production service.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/09-aws-verification.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/20-aws-eks-console.png

## 13 Cloud cleanup

The cleanup transcript records the destroy attempts and the final successful result. Session credentials expired during the first cleanup attempt. Rerunning destroy with automatic credential renewal removed the remaining resources. Terraform state list then returned no resources. AWS returned an empty cluster list, no matching VPC, and terminated status for both EC2 workers. The account remained on its Free plan. This is why infrastructure cleanup is part of the capstone verification instead of just a final command shown in documentation.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/10-terraform-destroy.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/23-terraform-destroy.png

## 14 Kubernetes and Helm

The Helm chart deploys into the campusdesk namespace. It includes frontend and backend Deployments, ClusterIP Services, PostgreSQL with persistent storage, an Ingress resource, and a backend HPA. The initial verification showed two frontend replicas, two backend replicas, and one PostgreSQL Pod running. Readiness controls when traffic can reach each workload. The database password comes from a Kubernetes Secret. Helm manages install and upgrade revisions. The recorded release reached revision three and used the exact SHA-tagged application images from GHCR. A single database replica is a classroom availability limit.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/06-helm-deployment.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/24-helm-pods-services.png

## 15 Ingress routing

An Ingress resource describes routing, while an Ingress controller actually handles traffic. The Nginx controller sends the root path to the frontend Service and /api to the backend Service. The browser uses relative API paths, so it never needs an internal cluster hostname. The local port forward exposes the controller on port 8088. The screenshot shows the application through campusdesk.localhost, including live ticket data fetched through the API route. The updated support-team description comes from the release installed during the recorded delivery demonstration.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/12-ingress-and-monitoring.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/25-ingress-application.png

## 16 Autoscaling under API load

The HPA uses CPU utilization with a target of fifty percent. Backend containers request fifty millicores of CPU, and Metrics Server supplies utilization measurements. The controlled load job sent real requests to the ticket API and completed 70,388 successful requests. The observed backend replica count rose from two to four. The chart compares those two observed states, rather than pretending to show a continuous time series. The transcript records CPU readings, the HPA successful rescale event, and four Running backend Pods. The load Job was deleted afterward, and the HPA returned the workload to its minimum as utilization fell.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/13-hpa-scaling.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/helm/campusdesk/templates/hpa.yaml

## 17 Prometheus target health

Prometheus runs in the monitoring namespace. Its application scrape job discovers backend Pods in the campusdesk namespace and keeps Running Pods with the backend label. It scrapes each target every five seconds. The Targets screenshot shows all four backend replicas UP during the autoscaling exercise. This verifies application scraping rather than just proving that the Prometheus server is installed. The final verification after release upgrades also checked healthy application targets. Metrics Server serves the HPA, while Prometheus serves application monitoring. Those are separate roles.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/12-ingress-and-monitoring.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/30-prometheus-targets.png

## 18 Live application metrics in Grafana

Grafana uses the in-cluster Prometheus datasource. The provisioned CampusDesk dashboard shows the sum of current backend HTTP request counters and request rate by endpoint. The screenshot contains actual API traffic from the load exercise. The request counter is process-local, so a restart can reset it, and summing counters across the currently running Pods can change during replacement. A rate query is useful for comparing incoming traffic over time. The local demonstration permits anonymous Viewer access, while the administrator password comes from a Kubernetes Secret.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/monitoring/campusdesk-dashboard.json
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/screenshots/31-grafana-dashboard.png

## 19 Troubleshooting and recovery

The isolated campusdesk-lab namespace kept the failure exercises separate from the application. A nonexistent image tag caused image pull failure. Pod events identified the missing tag, and correcting the image restored the Deployment. The second exercise created a Service selector that matched no Pods, leaving its EndpointSlice empty. Correcting the selector restored endpoints. The first immediate HTTP check still failed while routing converged, and the repeated check after reconciliation returned an actual response. The exercise namespace was removed after the verification. Explain how labels connect a Service to Pods.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/14-troubleshooting.txt
- https://github.com/Suhassk205/taskboard-capstone/tree/main/troubleshooting

## 20 Recorded release and live demo

The recorded walkthrough opens on the real commit output, follows the hosted pipeline, and then shows deployment of the exact published images on the laptop. The change updates the support-team description on the dashboard. The release commit is e3d1168, the full tag is e3d116880213a019f1af59caabdd48ce8fecf492, and the workflow run is 38953107445. Helm reaches revision three. The verification checks both the visible description and the embedded Git SHA in the deployed frontend asset. For a live presentation, open the application, show a ticket action, then use the recording for the delivery chain. Continue with the monitoring dashboard and troubleshooting evidence if requested. The repository includes a presentation guide with commands and discussion points.

Sources:
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/18-recorded-delivery.txt
- https://github.com/Suhassk205/taskboard-capstone/blob/main/evidence/campusdesk-delivery-walkthrough.mp4
- https://github.com/Suhassk205/taskboard-capstone/blob/main/docs/presentation-guide.md
