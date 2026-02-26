# 🐳 Docker Deployment Guide

This guide covers everything you need to know about running the Healthcare Chatbot using Docker.

## Why Use Docker?

- ✅ **No Python Setup Required**: No need to install Python or manage virtual environments
- ✅ **Consistent Environment**: Works the same on any machine (Linux, macOS, Windows)
- ✅ **Easy Deployment**: One command to start, one to stop
- ✅ **Isolated**: Doesn't interfere with other applications on your system
- ✅ **Portable**: Easy to deploy to cloud servers

## Prerequisites

Install Docker and Docker Compose:

### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Enable Docker service
sudo systemctl enable --now docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER
# Then log out and log back in
```

### macOS
Download and install [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)

### Windows
Download and install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Quick Start

### Using Docker Compose (Recommended)

1. **Start the application**:
   ```bash
   docker-compose up -d
   ```
   
   The `-d` flag runs it in detached mode (background).

2. **Access the application**:
   Open your browser to: `http://localhost:8501`

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```
   Press `Ctrl+C` to stop viewing logs (container keeps running).

4. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Using Docker Directly

1. **Build the image**:
   ```bash
   docker build -t healthcare-chatbot .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     -p 8501:8501 \
     --name healthcare-chatbot \
     -v $(pwd)/temp_uploads:/app/temp_uploads \
     healthcare-chatbot
   ```

3. **Stop the container**:
   ```bash
   docker stop healthcare-chatbot
   docker rm healthcare-chatbot
   ```

## Common Docker Commands

### Container Management
```bash
# Start existing container
docker start healthcare-chatbot

# Stop running container
docker stop healthcare-chatbot

# Restart container
docker restart healthcare-chatbot

# Remove container
docker rm healthcare-chatbot

# View running containers
docker ps

# View all containers (including stopped)
docker ps -a
```

### Logs and Monitoring
```bash
# View logs
docker logs healthcare-chatbot

# Follow logs in real-time
docker logs -f healthcare-chatbot

# View last 100 lines
docker logs --tail 100 healthcare-chatbot

# Check container resource usage
docker stats healthcare-chatbot

# Inspect container details
docker inspect healthcare-chatbot
```

### Image Management
```bash
# List images
docker images

# Remove image
docker rmi healthcare-chatbot

# Rebuild image (after code changes)
docker-compose build --no-cache

# Pull base images
docker pull python:3.12-slim
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (use `.env.example` as template):

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

The docker-compose.yml will automatically load variables from `.env`.

### Custom Port

To run on a different port:

**Docker Compose**: Edit `docker-compose.yml`
```yaml
ports:
  - "8080:8501"  # Change 8080 to your desired port
```

**Docker Command**:
```bash
docker run -d -p 8080:8501 --name healthcare-chatbot healthcare-chatbot
```

### Volume Mounts

Volumes persist data and allow live code updates:

```yaml
volumes:
  # For development - live code updates
  - ./src:/app/src
  - ./static:/app/static
  
  # Persist uploaded files
  - ./temp_uploads:/app/temp_uploads
```

## Development with Docker

### Live Code Reloading

1. **Ensure volumes are mounted** in docker-compose.yml (already configured)

2. **Run with Docker Compose**:
   ```bash
   docker-compose up
   ```

3. **Edit code**: Changes to files in `src/` and `static/` will be reflected automatically

4. **Streamlit auto-reloads** when it detects file changes

### Rebuilding After Changes

When you modify dependencies or Dockerfile:

```bash
# Stop and rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

Or in one command:
```bash
docker-compose up -d --build
```

## Production Deployment

### Building for Production

1. **Comment out development volumes** in docker-compose.yml:
   ```yaml
   volumes:
     # Development volumes (comment out for production)
     # - ./src:/app/src
     # - ./static:/app/static
     
     # Keep this for data persistence
     - ./temp_uploads:/app/temp_uploads
   ```

2. **Build and deploy**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

### Resource Limits

Add resource limits to docker-compose.yml:

```yaml
services:
  healthcare-chatbot:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Health Checks

The Dockerfile includes a health check. Monitor it:

```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' healthcare-chatbot

# View health check logs
docker inspect healthcare-chatbot | grep -A 10 Health
```

## Cloud Deployment

### Deploy to Docker Hub

1. **Tag the image**:
   ```bash
   docker tag healthcare-chatbot yourusername/healthcare-chatbot:latest
   ```

2. **Push to Docker Hub**:
   ```bash
   docker login
   docker push yourusername/healthcare-chatbot:latest
   ```

3. **Pull and run on any server**:
   ```bash
   docker pull yourusername/healthcare-chatbot:latest
   docker run -d -p 8501:8501 yourusername/healthcare-chatbot:latest
   ```

### Deploy to Cloud Platforms

**AWS ECS, Google Cloud Run, Azure Container Instances**: All support running Docker containers directly. Upload your image to their container registries and deploy.

**DigitalOcean App Platform**:
```bash
# Push to Docker Hub, then create app from Docker Hub image
```

**Heroku**:
```bash
heroku container:login
heroku container:push web -a your-app-name
heroku container:release web -a your-app-name
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs for errors
docker logs healthcare-chatbot

# Check if port is already in use
sudo lsof -i :8501
# Or on some systems:
sudo netstat -tulpn | grep 8501
```

### Permission Denied Errors

```bash
# Add your user to docker group (Linux)
sudo usermod -aG docker $USER
# Log out and log back in

# Or run with sudo (not recommended)
sudo docker-compose up -d
```

### Out of Disk Space

```bash
# Clean up unused containers, images, and volumes
docker system prune -a --volumes

# Remove only stopped containers
docker container prune

# Remove only unused images
docker image prune -a
```

### Application Not Accessible

1. Check if container is running:
   ```bash
   docker ps
   ```

2. Check port mapping:
   ```bash
   docker port healthcare-chatbot
   ```

3. Test from inside container:
   ```bash
   docker exec healthcare-chatbot curl http://localhost:8501
   ```

4. Check firewall settings (allow port 8501)

### Rebuilding After Errors

```bash
# Complete cleanup and rebuild
docker-compose down
docker system prune -f
docker-compose build --no-cache
docker-compose up -d
```

## Performance Tips

1. **Use Docker BuildKit** for faster builds:
   ```bash
   DOCKER_BUILDKIT=1 docker build -t healthcare-chatbot .
   ```

2. **Multi-stage builds**: The Dockerfile is optimized with proper layer caching

3. **Reduce image size**: Using `python:3.12-slim` instead of full Python image

4. **Monitor resources**:
   ```bash
   docker stats healthcare-chatbot
   ```

## Security Best Practices

1. **Don't run as root**: The container should run as non-root user (can be added to Dockerfile)

2. **Scan for vulnerabilities**:
   ```bash
   docker scan healthcare-chatbot
   ```

3. **Use specific versions**: Pin dependency versions in requirements files

4. **Keep Docker updated**: Regularly update Docker and base images

5. **Limit network exposure**: Only expose necessary ports

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
- [Best Practices for Docker](https://docs.docker.com/develop/dev-best-practices/)

---

Need help? Check the main [README.md](README.md) or create an issue!
