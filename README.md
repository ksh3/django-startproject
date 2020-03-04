# DJANGO START PROJECT

```
# Docker
docker-compose up -d
docker-compose stop

# Dev CLI

# Generate ER GRAPH.
./manage.py graph_models -a -g > .idea/er.dot && dot -Tpng .idea/er.dot > .idea/er.png

# Generate DJANGO ADMIN.
./manage.py admin_generator {app} > src/{app}/admin.py
```
