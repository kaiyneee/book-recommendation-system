from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Загружаем данные о книгах
books_df = pd.read_csv('books.csv')

# Заполняем пропущенные значения ПРАВИЛЬНО
books_df['authors'] = books_df['authors'].fillna('')

# Проверяем есть ли колонка 'genres' и обрабатываем ее
if 'genres' in books_df.columns:
    books_df['genres'] = books_df['genres'].fillna('')
else:
    # Если колонки нет - создаем пустую
    books_df['genres'] = ''

# Создаем контент для рекомендаций
books_df['content'] = books_df['authors'] + ' ' + books_df['genres']

# Простая функция рекомендаций (пока заглушка)
def get_recommendations(title):
    try:
        # Просто возвращаем первые 10 книг (кроме выбранной)
        other_books = books_df[books_df['title'] != title].head(10)
        return other_books['title'].tolist()
    except:
        # Если что-то пошло не так, возвращаем пустой список
        return []

@app.route('/')
def index():
    """Главная страница с поиском"""
    # Берем первые 50 книг для выпадающего списка
    book_titles = books_df['title'].head(50).tolist()
    return render_template('index.html', book_titles=book_titles)

@app.route('/recommend', methods=['POST'])
def recommend():
    """Обработка запроса на рекомендации"""
    book_title = request.form['book_title']
    
    try:
        recommendations = get_recommendations(book_title)
        
        return render_template('results.html', 
                             original_book=book_title,
                             recommendations=recommendations)
    
    except Exception as e:
        return f"Ошибка: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)