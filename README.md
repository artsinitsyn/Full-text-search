# Full-text-search
My simple library explorer. Using this application, you can organize a full-text search. The 20 best books of English literature are used as a library.The data is indexed in OpenSearch. The possibility of a faceted search has been implemented (group filtering of results by genre, year, and keywords).

Stack:
- Django REST Framework
- OpenSearch
- React with Material UI
- Docker

Adresses:
OpenSearch --> [port 9200](http://localhost:9200)

Backend (Django) --> [port 8000](http://localhost:8000/)

Frontend (React) --> [port 3000](http://localhost:3000)

End Point of Search --> [http://localhost:8000/api/search/?q=test]

Launch Guide (from the root of the project, works well on Ubuntu 24.04 LTS):
docker-compose up --build
cd backend

source venv/bin/activate

pip install requests faker

python generate_gutenberg_books.py

curl -X PUT "http://localhost:9200/books/_settings" \
  -H "Content-Type: application/json" \
  -d '{
    "index.highlight.max_analyzed_offset": 50000000
}'

curl "http://localhost:9200/books/_count"

cntr+d

docker-compose restart backend

cd ..

cd frontend

npm install

npm start




