# Marcela Vitor Learning Center

A Django-based web application for the Marcela Vitor Learning Center.

## Project Overview

This project is a web application for the Marcela Vitor Learning Center, built with Django and PostgreSQL. It includes features for managing course content, student registrations, and other learning center functionalities.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Setup with Docker

1. Clone the repository:
   ```
   git clone [repository-url]
   cd marcela_vitor_learning_center
   ```

2. Create a `.env` file with the necessary environment variables (example provided in the repository).

3. Start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

4. Run migrations to set up the database:
   ```
   docker exec -it marcela_vitor_learning_center-web-project-1 python manage.py migrate
   ```

5. Access the application at http://localhost:8000

### Using the Docker Management Script

For convenience, you can use the included `docker_manage.sh` script to manage the Docker containers:

```
./docker_manage.sh [OPTION]
```

Available options:
- `start`: Start the containers
- `stop`: Stop the containers
- `restart`: Restart the containers
- `rebuild`: Rebuild and restart the containers
- `logs`: Show logs from the web container
- `db-logs`: Show logs from the database container
- `migrate`: Run database migrations
- `shell`: Open a shell in the web container
- `db-shell`: Open a PostgreSQL shell
- `status`: Show container status
- `help`: Display help message

## Project Structure

- `app/`: Django project settings and configuration
- `website/`: Main Django application with models, views, and templates
- `templates/`: HTML templates for the web interface
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User-uploaded files
- `locale/`: Translation files

## Development

### Running in Development Mode

For development, you can use the included `docker-compose.yml` file:

```
docker-compose up -d
```

### Making Changes

1. Make your changes to the code
2. Rebuild the Docker containers:
   ```
   docker-compose down && docker-compose build && docker-compose up -d
   ```

### Applying Database Migrations

After making changes to models, create and apply migrations:

```
docker exec -it marcela_vitor_learning_center-web-project-1 python manage.py makemigrations
docker exec -it marcela_vitor_learning_center-web-project-1 python manage.py migrate
```

## Troubleshooting

### Common Issues

1. **Database connection issues**
   - Check that the database container is running: `docker ps`
   - Verify environment variables in the `.env` file

2. **Container startup problems**
   - Check container logs: `docker logs marcela_vitor_learning_center-web-project-1`
   - Ensure the web container waits for the database to be ready

3. **Application errors**
   - Check the web application logs for error messages
   - Verify that migrations have been applied

### Getting Help

If you encounter issues not covered here, please contact the project maintainers.