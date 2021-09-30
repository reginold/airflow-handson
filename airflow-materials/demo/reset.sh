# Startup all the containers without cache
docker-compose rm --all &&
docker-compose pull &&
docker-compose build --no-cache &&
docker-compose up -d --force-recreate

# /!\ WARNING: RESET EVERYTHING! 
# Remove all containers/networks/volumes/images and data in db
# docker-compose down
# docker system prune -f
# docker volume prune -f
# docker network prune -f
# docker rmi -f $(docker images -a -q)

