"""
Библиотечная система управления.

Этот модуль предоставляет функциональность для управления библиотекой книг.
Он позволяет добавлять книги, удалять книги, искать книги по различным критериям,
отображать все книги и изменять статус книги.

Функции:
    - load_data(): Загружает данные о книгах из файла JSON.
    - save_data(books): Сохраняет данные о книгах в файл JSON.
    - add_book(title, author, year): Добавляет новую книгу в библиотеку.
    - delete_book(book_id): Удаляет книгу из библиотеки по её ID.
    - find_books(query, field): Ищет книги по заданному запросу и полю.
    - display_books(): Отображает все книги в библиотеке.
    - change_status(book_id, new_status): Изменяет статус книги по её ID.
    - main(): Главная функция, которая запускает интерактивное меню.

Переменные:
    - DATABASE_PATH: Путь к файлу JSON, где хранятся данные о книгах.

Пример использования:
    python library_management_system.py
"""


import json
from os import path
from typing import List, Dict, Union
from uuid import uuid4

DATABASE_PATH = 'database.json'

def load_data() -> List[Dict[str, Union[str, int]]]:
    """
        Загружает данные о книгах из файла JSON.

        Returns:
            List[Dict[str, Union[str, int]]]: Список книг, где каждая книга представлена словарем.
        """
    if not path.exists(DATABASE_PATH):
        return []
    try:
        with open(DATABASE_PATH, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (IOError, json.JSONDecodeError):
        print("Ошибка при загрузке данных из файла.")
        return []

def save_data(books: List[Dict[str, Union[str, int]]]) -> None:
    """
        Сохраняет данные о книгах в файл JSON.

        Args:
            books (List[Dict[str, Union[str, int]]]): Список книг для сохранения.
        """
    try:
        with open(DATABASE_PATH, 'w', encoding='utf-8') as file:
            json.dump(books, file, ensure_ascii=False, indent=2)
    except IOError:
        print("Ошибка при сохранении данных в файл.")

def add_book(title: str, author: str, year: int) -> Union[str, None]:
    """
        Добавляет новую книгу в библиотеку.

        Args:
            title (str): Название книги.
            author (str): Автор книги.
            year (int): Год издания книги.

        Returns:
            Union[str, None]: ID добавленной книги или None, если возникла ошибка.
        """
    try:
        books = load_data()
        book_id = str(uuid4())
        new_book = {
            'id': book_id,
            'title': title,
            'author': author,
            'year': int(year),
            'status': 'в наличии'
        }
        books.append(new_book)
        save_data(books)
        return book_id
    except ValueError:
        print("Неверный формат года издания. Пожалуйста, введите число.")
        return None

def delete_book(book_id: str) -> None:
    """
        Удаляет книгу из библиотеки по её ID.

        Args:
            book_id (str): ID книги для удаления.
        """
    books = load_data()
    initial_length = len(books)
    books = [book for book in books if book['id'] != book_id]
    if len(books) == initial_length:
        print("Книга с указанным ID не найдена.")
    else:
        save_data(books)
        print("Книга успешно удалена.")

def find_books(query: str, field: str) -> List[Dict[str, Union[str, int]]]:
    """
        Ищет книги по заданному запросу и полю.

        Args:
            query (str): Запрос для поиска.
            field (str): Поле, по которому выполняется поиск ('title', 'author' или 'year').

        Returns:
            List[Dict[str, Union[str, int]]]: Список найденных книг.
        """
    books = load_data()
    if not field:
        field = 'title'
    if field not in ['title', 'author', 'year']:
        print("Неверное поле для поиска. Пожалуйста, выберите 'title', 'author' или 'year'.")
        return []
    result = [
        book for book in books
        if str(query).lower() in str(book[field]).lower()
    ]
    return result

def display_books() -> None:
    """
        Отображает все книги в библиотеке.
        """
    books = load_data()
    if not books:
        print("Библиотека пуста.")
    else:
        for book in books:
            print(
                f"ID: {book['id']}, Название: {book['title']}, "
                f"Автор: {book['author']}, Год: {book['year']}, "
                f"Статус: {book['status']}"
            )

def change_status(book_id: str, new_status: str) -> None:
    """
        Изменяет статус книги по её ID.

        Args:
            book_id (str): ID книги для изменения статуса.
            new_status (str): Новый статус книги ('в наличии' или 'выдана').
        """
    books = load_data()
    book_found = False
    for book in books:
        if book['id'] == book_id:
            if new_status not in ['в наличии', 'выдана']:
                print("Неверный статус. Пожалуйста, выберите 'в наличии' или 'выдана'.")
                return
            book['status'] = new_status
            book_found = True
            break
    if not book_found:
        print("Книга с указанным ID не найдена.")
    else:
        save_data(books)
        print("Статус книги успешно изменен.")

def main():
    print("Добро пожаловать в систему управления библиотекой!")
    while True:
        print("\nВыберите действие:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Введите номер действия: ")

        try:
            if choice == '1':
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = input("Введите год издания книги: ")
                book_id = add_book(title, author, year)
                if book_id:
                    print(f"Книга успешно добавлена. ID: {book_id}")
            elif choice == '2':
                book_id = input("Введите ID книги для удаления: ")
                delete_book(book_id)
            elif choice == '3':
                query = input("Введите запрос для поиска (название, автор или год): ")
                field = input("Введите поле для поиска (title, author или year): ")
                books = find_books(query, field)
                if not books:
                    print("Книги не найдены.")
                else:
                    for book in books:
                        print(
                            f"ID: {book['id']}, Название: {book['title']}, "
                            f"Автор: {book['author']}, Год: {book['year']}, "
                            f"Статус: {book['status']}"
                        )
            elif choice == '4':
                display_books()
            elif choice == '5':
                book_id = input("Введите ID книги для изменения статуса: ")
                new_status = input("Введите новый статус (в наличии или выдана): ")
                change_status(book_id, new_status)
            elif choice == '6':
                print("До свидания!")
                break
            else:
                print("Неверный номер действия. Пожалуйста, попробуйте снова.")
        except KeyboardInterrupt:
            print("\nПрограмма прервана пользователем. До свидания!")
            break


if __name__ == '__main__':
    main()