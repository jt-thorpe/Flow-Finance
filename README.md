# Flow-Finance
A personal finance and budgeting web application for the Mrs and I.

## Docker
### Image
Build the image with: `docker build -t flow-finance .`

### Container
Run the container with: `docker run -d -p 5000:5000 -e FLOW_DB_URI="DB_URI_HERE" flow-finance`

## Accessing the app
Currently accessed locally at: `http://127.0.0.1:5000/`