from flask import Flask,render_template,request
from flask import redirect, url_for

import pickle
import pandas as pd
from patsy import dmatrices
import numpy as np



with open('models/books.pkl', 'rb') as file:
    books = pd.read_pickle(file)
similarity=pd.read_pickle(open('models/cosine_sim.pkl','rb'))
pt=pd.read_pickle(open('models/bpivot.pkl','rb'))
popular_df=pd.read_pickle(open('models/popular.pkl','rb'))
hybrid=pd.read_pickle(open('models/hybrid_recommendations.pkl','rb'))
samep=pd.read_pickle(open('models/recommended_book.pkl','rb'))
book3=pd.read_pickle(open('models/book3.pkl','rb'))
 

app = Flask(__name__)

@app.route('/')
def Home():
    return render_template("index.html")

@app.route('/About')
def popular():
    return render_template("popular.html",
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_rating'].values),
                           rating=list(popular_df['avg_rating'].values)
                            )

@app.route('/Contact')
def Contact():
    return render_template("contact.html")

@app.route('/Recommendation')
def Recommendation():
    
    return render_template("about.html")

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

@app.route('/author_ui')
def author_ui():
    all_authors = book3['Book-Author'].unique()
    return render_template('author.html', authors=all_authors, books=books)

@app.route('/author_books', methods=['GET', 'POST'])
def author_books():
    if request.method == 'POST':
        author_name = request.form.get('author_name')
        author_books = book3[book3['Book-Author'] == author_name].head(5)
        return render_template('books_by_author.html', author_name=author_name, books=author_books)
    else:
        return redirect(url_for('author_ui'))

@app.route('/publisher_ui')
def publisher_ui():
    all_publishers = books['Publisher'].unique()
    return render_template('publisher.html', publishers=all_publishers, books=books)

@app.route('/publisher_books', methods=['GET', 'POST'])
def publisher_books():
    if request.method == 'POST':
        publisher_name = request.form.get('publisher_name')
        publisher_books = books[books['Publisher'] == publisher_name].head(5)
        return render_template('books_by_publisher.html', publisher_name=publisher_name, books=publisher_books)
    else:
        return redirect(url_for('publisher_ui'))
    
@app.route('/isbn_ui')
def isbn_ui():
    all_isbn = book3['ISBN'].unique()
    return render_template('isbn.html', isbn=all_isbn, books=books)

@app.route('/isbn_books', methods=['GET', 'POST'])
def isbn_books():
    if request.method == 'POST':
        isbn_name = request.form.get('isbn_name')
        isbn_books = book3[book3['ISBN'] == isbn_name].head(1)
        return render_template('books_on_isbn.html', isbn_name=isbn_name, books=isbn_books)
    else:
        return redirect(url_for('isbn_ui'))    

if __name__ == '__main__':
    app.debug= True
    app.run()