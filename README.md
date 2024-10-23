# Flow-Finance
***Under Development***

A personal finance and budgeting web application for the Mrs and I. I was originally developing a desktop application but decided for ease-of-use for us, a web application would be better. In addition the project is an opportunity develop and improve my full-stack web development skills.

This README is currently more a collection of notes for myself rather than anything particularly useful.

## Docker
### Image
Build the image with:
```
docker build -t flow-finance:<tag_here> .
```

### Container
Run the container with: 
```
docker run -d -p 5000:5000 \
           --name flow-dev-<tag_here> \
           -v /home/jake/projects/Flow-Finance/:/app \
           -e FLOW_DB_URI="flow_db_uri_here" \
           -e JWT_SECRET_KEY="super_secret_test_key" \
           flow-finance:<tag_here>
```

## Accessing the app
Currently accessed locally at: `http://127.0.0.1:5000/`
