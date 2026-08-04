# Development Environment

This runbook documents how to start the EventNexus Hanke Keskond stack in development mode with hot reload, bind mounts, and a local test mail server.

## Prerequisites

- Docker Engine 24+ and Docker Compose V2 plugin
- Git
- A shell: PowerShell 5.1+ on Windows, or Bash on Linux/macOS/WSL

## Environment file

Copy the example environment file and fill in the required values:

```bash
cp apps/api/.env.example apps/api/.env
```

Minimum required variables for local development:

- `POSTGRES_PASSWORD`
- `MINIO_ROOT_PASSWORD`
- `SECRET_KEY` (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)

## Starting development mode

Development mode uses `docker-compose.dev.yml` as a Compose override on top of the base `docker-compose.yml`. This adds:

- bind mounts for `apps/web`, `apps/api`, and `apps/worker`
- hot-reload for the API, worker, and Next.js dev server
- a MailHog test mail server on `localhost:8025`

### Bash

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Detached:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
```

Stop:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```

### PowerShell

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

Detached:

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
```

Stop:

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml down
```

## Test mail

MailHog captures all emails sent by the application during development.

- SMTP: `localhost:1025`
- Web UI: `http://localhost:8025`

Configure application mail settings to use `mailhog:1025` as the SMTP host when running inside Docker, or `localhost:1025` when sending from the host machine directly.

## Hot reload behavior

| Service | Mount | Reload mechanism |
|---|---|---|
| web | `./apps/web:/app` with preserved `/app/node_modules` and `/.next` | Next.js dev server watches source files |
| api | `./apps/api:/app` | `uvicorn --reload` restarts on Python file changes |
| worker | `./apps/worker:/app` | `uvicorn --factory --reload` restarts on Python file changes |

## Verifying the stack

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml ps
```

Expected running services: `web`, `api`, `worker`, `postgres`, `redis`, `minio`, `db-init`, `minio-init`, `mailhog`.

Health endpoints:

- Web: `http://localhost:3000/api/health`
- API: `http://localhost:8000/health`
- Worker: `http://localhost:8001/health`
- MailHog UI: `http://localhost:8025`

## Production-like mode (no hot reload)

Run the base compose file without the dev override to use the production-like images and commands:

```bash
# Bash
docker compose up --build -d

# PowerShell
docker compose up --build -d
```

This uses the built image layers without source-code bind mounts. Code changes require an image rebuild.
