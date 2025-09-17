#!/bin/bash
# Docker management script for Marcela Vitor Learning Center

# Set working directory
cd "$(dirname "$0")"

# Function to display help message
show_help() {
  echo "Usage: ./docker_manage.sh [OPTION]"
  echo "Management script for Docker containers."
  echo ""
  echo "Options:"
  echo "  start       Start the containers"
  echo "  stop        Stop the containers"
  echo "  restart     Restart the containers"
  echo "  rebuild     Rebuild and restart the containers"
  echo "  logs        Show logs from the web container"
  echo "  db-logs     Show logs from the database container"
  echo "  migrate     Run database migrations"
  echo "  shell       Open a shell in the web container"
  echo "  db-shell    Open a PostgreSQL shell"
  echo "  status      Show container status"
  echo "  help        Display this help message"
  echo ""
}

# Function to check if containers are running
check_running() {
  if [ "$(docker ps -q -f name=marcela_vitor_learning_center-web-project)" ]; then
    return 0
  else
    return 1
  fi
}

# Main script logic
case "$1" in
  start)
    echo "Starting containers..."
    docker-compose up -d
    ;;
  stop)
    echo "Stopping containers..."
    docker-compose down
    ;;
  restart)
    echo "Restarting containers..."
    docker-compose down && docker-compose up -d
    ;;
  rebuild)
    echo "Rebuilding and restarting containers..."
    docker-compose down && docker-compose build && docker-compose up -d
    ;;
  logs)
    echo "Showing web container logs..."
    docker logs -f marcela_vitor_learning_center-web-project-1
    ;;
  db-logs)
    echo "Showing database container logs..."
    docker logs -f learning-center-database
    ;;
  migrate)
    echo "Running database migrations..."
    if check_running; then
      docker exec -it marcela_vitor_learning_center-web-project-1 python manage.py migrate
    else
      echo "Web container is not running. Start it first with './docker_manage.sh start'"
    fi
    ;;
  shell)
    echo "Opening shell in web container..."
    if check_running; then
      docker exec -it marcela_vitor_learning_center-web-project-1 bash
    else
      echo "Web container is not running. Start it first with './docker_manage.sh start'"
    fi
    ;;
  db-shell)
    echo "Opening PostgreSQL shell..."
    if check_running; then
      docker exec -it learning-center-database psql -U postgres -d learning_center
    else
      echo "Database container is not running. Start it first with './docker_manage.sh start'"
    fi
    ;;
  status)
    echo "Container status:"
    docker ps -a | grep -E 'marcela_vitor_learning_center-web-project|learning-center-database'
    ;;
  help|*)
    show_help
    ;;
esac
