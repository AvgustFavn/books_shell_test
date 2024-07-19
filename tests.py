import io
import json
import sys
import unittest
import os
import tempfile
import uuid
from datetime import datetime
from main import load_data, save_data, add_book, delete_book, find_books, display_books, change_status

class TestBookFunctions(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.DATABASE_PATH = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        os.remove(self.DATABASE_PATH)

    def test_load_data(self):
        # Проверяем, что функция возвращает пустой список, если файл не существует
        self.assertEqual(load_data(), [])

        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'}]
        save_data(sample_data)

        # Проверяем, что функция загружает данные из файла
        self.assertEqual(load_data(), sample_data)

    def test_save_data(self):
        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'}]
        save_data(sample_data)

        # Проверяем, что данные сохранились в файле
        with open(self.DATABASE_PATH, 'r', encoding='utf-8') as file:
            self.assertEqual(json.load(file), sample_data)

    def test_add_book(self):
        # Добавляем новую книгу
        book_id = add_book('Book 1', 'Author 1', 2000)
        self.assertIsNotNone(book_id)

        # Проверяем, что книга сохранилась в файле
        books = load_data()
        self.assertEqual(books[0]['id'], book_id)
        self.assertEqual(books[0]['title'], 'Book 1')
        self.assertEqual(books[0]['author'], 'Author 1')
        self.assertEqual(books[0]['year'], 2000)
        self.assertEqual(books[0]['status'], 'в наличии')

    def test_delete_book(self):
        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'}]
        save_data(sample_data)

        # Удаляем книгу
        delete_book(sample_data[0]['id'])

        # Проверяем, что книга удалена из файла
        books = load_data()
        self.assertEqual(len(books), 0)

    def test_find_books(self):
        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'},
                       {'id': str(uuid.uuid4()), 'title': 'Book 2', 'author': 'Author 2', 'year': 2001, 'status': 'в наличии'}]
        save_data(sample_data)

        # Ищем книгу по названию
        found_books = find_books('Book 1', 'title')
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0]['title'], 'Book 1')

        # Ищем книгу по автору
        found_books = find_books('Author 2', 'author')
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0]['author'], 'Author 2')

        # Ищем книгу по году
        found_books = find_books('2000', 'year')
        self.assertEqual(len(found_books), 1)
        self.assertEqual(found_books[0]['year'], 2000)

        # Ищем книгу по несуществующему полю
        found_books = find_books('Test', 'test')
        self.assertEqual(len(found_books), 0)

    def test_display_books(self):
        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'},
                       {'id': str(uuid.uuid4()), 'title': 'Book 2', 'author': 'Author 2', 'year': 2001, 'status': 'в наличии'}]
        save_data(sample_data)

        # Отображаем книги
        captured_output = io.StringIO()
        sys.stdout = captured_output
        display_books()
        sys.stdout = sys.__stdout__

        # Проверяем, что книги отобразились корректно
        for book in sample_data:
            self.assertIn(book['id'], captured_output.getvalue())
            self.assertIn(book['title'], captured_output.getvalue())
            self.assertIn(book['author'], captured_output.getvalue())
            self.assertIn(str(book['year']), captured_output.getvalue())
            self.assertIn(book['status'], captured_output.getvalue())

    def test_change_status(self):
        # Сохраняем данные в файл
        sample_data = [{'id': str(uuid.uuid4()), 'title': 'Book 1', 'author': 'Author 1', 'year': 2000, 'status': 'в наличии'}]
        save_data(sample_data)

        # Изменяем статус книги
        change_status(sample_data[0]['id'], 'выдана')

        # Проверяем, что статус книги изменился
        books = load_data()
        self.assertEqual(books[0]['status'], 'выдана')

if __name__ == '__main__':
    unittest.main()