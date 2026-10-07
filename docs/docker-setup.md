# Docker setup and starting crAPI

Phase 1 needs crAPI running on your own computer. crAPI is intentionally vulnerable, so only run it locally and never expose it to the internet.

## 1. Install Docker

- **Windows:** install Docker Desktop (it uses WSL 2; the installer will guide you). Restart when asked.
- **macOS:** install Docker Desktop.
- **Linux:** install Docker Engine and the compose plugin using your distribution's official Docker instructions.

Official install pages: https://docs.docker.com/get-docker/

Check it works:

```
docker --version
docker compose version
docker run hello-world
```

Give Docker at least 4 GB of RAM (Docker Desktop: Settings > Resources). crAPI runs several containers.

## 2. Start crAPI

The steps below follow crAPI's published instructions. If something differs, the crAPI README on GitHub (OWASP/crAPI) is the source of truth.

```
mkdir crapi && cd crapi
curl -o docker-compose.yml https://raw.githubusercontent.com/OWASP/crAPI/main/deploy/docker/docker-compose.yml
docker compose pull
docker compose -f docker-compose.yml --compatibility up -d
```

First start can take a few minutes. Then open:

- App: http://localhost:8888
- Test mailbox (MailHog): http://localhost:8025

Sign up once in the browser to confirm it works.

## 3. Stop or reset

```
docker compose -f docker-compose.yml down        # stop
docker compose -f docker-compose.yml down -v     # stop and wipe data
```

## 4. Run the tests

From the `crapi-qa-platform` folder, see the README quick start.
