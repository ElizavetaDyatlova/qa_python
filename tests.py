import pytest
from main import BooksCollector


class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("name", ["Гарри Поттер", "Война и мир"])
    def test_add_new_book_valid_name_positive(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre
        assert collector.books_genre[name] == ""

    @pytest.mark.parametrize("name", ["А" * 41, ""])
    def test_add_new_book_valid_name_negative(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book("Война и мир")
        collector.add_new_book("Война и мир")
        assert len(collector.books_genre) == 1
        assert "Война и мир" in collector.books_genre

    @pytest.mark.parametrize("genre, book_exists, expected_genre", [
        ("Фантастика", True, "Фантастика"),
        ("Роман", True, ""),
        ("Фантастика", False, ""),
    ])
    def test_set_book_genre(self, genre, book_exists, expected_genre):
        collector = BooksCollector()
        book_name = "Книга"
        if book_exists:
            collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        if book_exists:
            assert collector.books_genre[book_name] == expected_genre
        else:
            assert collector.books_genre == {}

    @pytest.mark.parametrize("book_name, expected_genre", [
        ("Существующая книга", "Фантастика"),
        ("Нет такой книги", None),
    ])
    def test_get_book_genre(self, book_name, expected_genre):
        collector = BooksCollector()
        if book_name == "Существующая книга":
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, "Фантастика")
        genre = collector.get_book_genre(book_name)
        assert genre == expected_genre

    @pytest.mark.parametrize("genre, expected_books", [
        ("Комедии", ["Книга 1", "Книга 3"]),
        ("Детективы", []),
        ("Роман", []),
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Комедии")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 2", "Ужасы")
        collector.add_new_book("Книга 3")
        collector.set_book_genre("Книга 3", "Комедии")
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected_books

    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.set_book_genre("Книга 1", "Фантастика")
        collector.add_new_book("Книга 2")
        collector.set_book_genre("Книга 2", "Комедии")
        expected = {"Книга 1": "Фантастика", "Книга 2": "Комедии"}
        assert collector.get_books_genre() == expected

    @pytest.mark.parametrize("genre, should_be_in_children", [
        ("Фантастика", True),
        ("Мультфильмы", True),
        ("Комедии", True),
        ("Ужасы", False),
        ("Детективы", False),
        ("", False),
    ])
    def test_get_books_for_children(self, genre, should_be_in_children):
        collector = BooksCollector()
        book_name = "Детская книга"
        collector.add_new_book(book_name)
        if genre:
            collector.set_book_genre(book_name, genre)
        children_books = collector.get_books_for_children()
        if should_be_in_children:
            assert book_name in children_books
        else:
            assert book_name not in children_books

    @pytest.mark.parametrize("book_exists, already_favorite, expected_len", [
        (True, False, 1),
        (True, True, 1),
        (False, False, 0),
    ])
    def test_add_book_in_favorites(self, book_exists, already_favorite, expected_len):
        collector = BooksCollector()
        book_name = "Любимая книга"
        if book_exists:
            collector.add_new_book(book_name)
            if already_favorite:
                collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        assert len(collector.favorites) == expected_len
        if expected_len > 0:
            assert book_name in collector.favorites

    @pytest.mark.parametrize("book_in_favorites", [True, False])
    def test_delete_book_from_favorites(self, book_in_favorites):
        collector = BooksCollector()
        book_name = "Книга"
        collector.add_new_book(book_name)
        if book_in_favorites:
            collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites
        assert collector.favorites == []

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 2")
        collector.add_book_in_favorites("Книга 1")
        collector.add_book_in_favorites("Книга 2")
        favorites = collector.get_list_of_favorites_books()
        assert favorites == ["Книга 1", "Книга 2"]