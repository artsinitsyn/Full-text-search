# Full-text-search
My simple library explorer. Using this application, you can organize a full-text search. The 20 best books of English literature are used as a library.The data is indexed in OpenSearch. The possibility of a faceted search has been implemented (group filtering of results by genre, year, and keywords).

App testing --> [video](https://drive.google.com/file/d/16ewltCEgboC2UQvLKUNbcHeSTDAnhq-B/view?usp=sharing)

![Application design](https://drive.google.com/file/d/10IWq6bbJeD5M9KGoVSfv_D0ATG54-KrG/view?usp=sharing/Screenshot_from_2025-10-24_14-04-54.png)

**Stack:**
- Django REST Framework
- OpenSearch
- React with Material UI
- Docker

**Adresses:**
OpenSearch --> [port 9200](http://localhost:9200)

Backend (Django) --> [port 8000](http://localhost:8000/)

Frontend (React) --> [port 3000](http://localhost:3000)

End Point of Search --> [test](http://localhost:8000/api/search/?q=test)


**Launch Guide** (from the root of the project, works well on Ubuntu 24.04 LTS, something may need depands with your system):

```docker-compose up --build```

```cd backend```

```source venv/bin/activate```

```pip install requests faker```

```python generate_gutenberg_books.py```

```
curl -X PUT "http://localhost:9200/books/_settings" \
  -H "Content-Type: application/json" \
  -d '{
    "index.highlight.max_analyzed_offset": 50000000
}'
```

```curl "http://localhost:9200/books/_count"```

```Cntr+D```

```docker-compose restart backend```

```cd ..```

```cd frontend```

```npm install```

```npm start```




