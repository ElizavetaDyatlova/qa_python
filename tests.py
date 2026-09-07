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

    def test_initial_state(self):
        collector = BooksCollector()
        assert collector.books_genre == {}
        assert collector.favorites == []
        assert collector.genre == ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        assert collector.genre_age_rating == ['Ужасы', 'Детективы']

    @pytest.mark.parametrize("name", ["Книга", "Война и мир", "Гарри Поттер"])
    def test_add_new_book_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre
        assert collector.books_genre[name] == ''

    @pytest.mark.parametrize("name", ["", "А" * 41])
    def test_add_new_book_invalid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.books_genre

    def test_add_new_book_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book("Книга")
        collector.add_new_book("Книга")
        assert len(collector.books_genre) == 1
        assert "Книга" in collector.books_genre

    def test_set_book_genre_valid_for_existing_book(self):
        collector = BooksCollector()
        book_name = "Книга"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.books_genre.get(book_name) == "Фантастика"

    def test_set_book_genre_invalid_for_existing_book(self):
        collector = BooksCollector()
        book_name = "Книга"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Роман")
        assert collector.books_genre.get(book_name) == ""

    def test_set_book_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        book_name = "Книга"
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.books_genre == {}

    def test_get_book_genre_existing(self):
        collector = BooksCollector()
        book_name = "Существующая"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Фантастика")
        assert collector.get_book_genre(book_name) == "Фантастика"

    def test_get_book_genre_nonexistent(self):
        collector = BooksCollector()
        book_name = "Отсутствующая"
        assert collector.get_book_genre(book_name) is None

    @pytest.mark.parametrize("genre, expected_books", [
        ("Комедии", ["Книга1", "Книга3"]),
        ("Ужасы", ["Книга2"]),
        ("Детективы", []),
        ("Роман", []),
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Комедии")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Ужасы")
        collector.add_new_book("Книга3")
        collector.set_book_genre("Книга3", "Комедии")
        result = collector.get_books_with_specific_genre(genre)
        assert result == expected_books

    def test_get_books_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.set_book_genre("Книга1", "Фантастика")
        collector.add_new_book("Книга2")
        collector.set_book_genre("Книга2", "Мультфильмы")
        expected = {"Книга1": "Фантастика", "Книга2": "Мультфильмы"}
        assert collector.get_books_genre() == expected

    def test_get_books_for_children_unsuitable_genre(self):
        collector = BooksCollector()
        book_name = "Детская книга"
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, "Ужасы")
        assert book_name not in collector.get_books_for_children()

    def test_get_books_for_children_no_genre(self):
        collector = BooksCollector()
        book_name = "Детская книга"
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_for_children()

    def test_add_book_in_favorites_existing_not_favorite(self):
        collector = BooksCollector()
        book_name = "Любимая книга"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        assert len(collector.favorites) == 1
        assert book_name in collector.favorites

    def test_add_book_in_favorites_existing_already_favorite(self):
        collector = BooksCollector()
        book_name = "Любимая книга"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        assert len(collector.favorites) == 1
        assert book_name in collector.favorites

    def test_add_book_in_favorites_nonexistent(self):
        collector = BooksCollector()
        book_name = "Несуществующая книга"
        collector.add_book_in_favorites(book_name)
        assert len(collector.favorites) == 0
        assert book_name not in collector.favorites

    def test_delete_book_from_favorites_when_in_favorites(self):
        collector = BooksCollector()
        book_name = "Книга"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites
        assert collector.favorites == []

    def test_delete_book_from_favorites_when_not_in_favorites(self):
        collector = BooksCollector()
        book_name = "Книга"
        collector.add_new_book(book_name)
        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.favorites
        assert collector.favorites == []

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book("Книга1")
        collector.add_new_book("Книга2")
        collector.add_book_in_favorites("Книга1")
        collector.add_book_in_favorites("Книга2")
        assert collector.get_list_of_favorites_books() == ["Книга1", "Книга2"]