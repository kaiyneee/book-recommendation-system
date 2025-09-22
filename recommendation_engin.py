import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Загружаем данные о книгах
books_df = pd.read_csv('books.csv')

# Для примера, давайте посмотрим на структуру данных
print(books_df.head())
print(books_df.columns)

# Продолжение кода (добавь после предыдущего)

# Заполняем пропущенные значения
books_df['authors'] = books_df['authors'].fillna('')
# Проверим, есть ли колонка 'genres'
if 'genres' in books_df.columns:
    books_df['genres'] = books_df['genres'].fillna('')
else:
    # Если нет колонки 'genres', создадим пустую
    books_df['genres'] = ''

# Создаем контент для рекомендаций
books_df['content'] = books_df['authors'] + ' ' + books_df['genres']

# Векторизация
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books_df['content'])

print(f"Матрица признаков: {tfidf_matrix.shape}")

# Расчет схожести
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print(f"Матрица схожести: {cosine_sim.shape}")

# Функция рекомендаций
indices = pd.Series(books_df.index, index=books_df['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Топ-10 (исключая саму книгу)
        book_indices = [i[0] for i in sim_scores]
        return books_df['title'].iloc[book_indices]
    except KeyError:
        return "Книга не найдена!"

# Тестируем
print("\n=== ТЕСТ РЕКОМЕНДАЦИЙ ===")
test_book = books_df.iloc[0]['title']  # Берем первую книгу из датасета
print(f"Рекомендации для: {test_book}")
recommendations = get_recommendations(test_book)
print(recommendations)
