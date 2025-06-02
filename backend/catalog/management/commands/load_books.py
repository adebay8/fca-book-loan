import csv
from django.core.management.base import BaseCommand

from catalog.models import Book, Author, BookItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = "books.csv"
        count = 0

        with open(path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                isbn = row["ISBN"].strip()
                title = row["Title"].strip()
                pub_year = int(row["Publication Year"].strip())
                language = row["Language"].strip()
                authors_raw = row["Authors"].strip()

                book, created = Book.objects.get_or_create(
                    isbn=isbn,
                    defaults={
                        "title": title,
                        "publication_year": pub_year,
                        "language": language,
                    },
                )

                if not BookItem.objects.filter(book=book, is_available=True).exists():
                    BookItem.objects.create(book=book)

                if not created:
                    self.stdout.write(f"Skipping existing book: {title}")
                    continue

                author_names = [
                    name.strip() for name in authors_raw.split(",") if name.strip()
                ]
                for name in author_names:
                    author, _ = Author.objects.get_or_create(name=name)
                    book.authors.add(author)

                count += 1
                self.stdout.write(f"Added: {title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully added {count} books"))
