import requests
import json
import random
from faker import Faker

fake = Faker()

books_info = [
    (1342, "Pride and Prejudice", "Jane Austen", 1813, "Romance"),
    (84, "Frankenstein", "Mary Shelley", 1818, "Horror"),
    (2701, "Moby Dick", "Herman Melville", 1851, "Adventure"),
    (98, "A Tale of Two Cities", "Charles Dickens", 1859, "Historical Fiction"),
    (1661, "The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 1892, "Mystery"),
    (11, "Alice’s Adventures in Wonderland", "Lewis Carroll", 1865, "Fantasy"),
    (345, "Dracula", "Bram Stoker", 1897, "Horror"),
    (174, "The Picture of Dorian Gray", "Oscar Wilde", 1890, "Gothic Fiction"),
    (1080, "A Modest Proposal", "Jonathan Swift", 1729, "Satire"),
    (5200, "Metamorphosis", "Franz Kafka", 1915, "Absurdist Fiction"),
    (64317, "The Great Gatsby", "F. Scott Fitzgerald", 1925, "Novel"),
    (3207, "War and Peace", "Leo Tolstoy", 1869, "Historical Fiction"),
    (1400, "Great Expectations", "Charles Dickens", 1861, "Novel"),
    (768, "Wuthering Heights", "Emily Brontë", 1847, "Gothic Romance"),
    (2265, "The Time Machine", "H. G. Wells", 1895, "Science Fiction"),
    (36, "The War of the Worlds", "H. G. Wells", 1898, "Science Fiction"),
    (1952, "The Yellow Wallpaper", "Charlotte Gilman", 1892, "Psychological Horror"),
    (28054, "The Call of the Wild", "Jack London", 1903, "Adventure"),
    (159, "The Scarlet Letter", "Nathaniel Hawthorne", 1850, "Drama"),
    (23, "The Odyssey", "Homer", -800, "Epic Poetry"),
]

def download_text(gutenberg_id):
    urls = [
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}-0.txt",
        f"https://www.gutenberg.org/files/{gutenberg_id}/{gutenberg_id}.txt",
    ]
    for url in urls:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text.strip()
    return None

with open("books.jsonl", "w", encoding="utf-8") as f:
    for i, (gid, title, author, year, genre) in enumerate(books_info, start=1):
        print(f"Downloading {title} ...")
        text = download_text(gid)
        if not text:
            print(f"Failed: {title}")
            continue

        book = {
            "id": i,
            "title": title,
            "author": author,
            "genre": genre,
            "year": year,
            "content": text,
        }

        meta = {"index": {"_index": "books", "_id": i}}
        f.write(json.dumps(meta) + "\n")
        f.write(json.dumps(book) + "\n")

print("books.jsonl created! You can bulk-upload it to OpenSearch.")

