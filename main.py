from flask import Flask, request, render_template, session, redirect, abort
import json

app = Flask(__name__)



categories = [
    {
        'name': 'Фанфики про Лунтика',
        'fanfics': [
            {
                'name': 'Лунтик в Костроме',
                'likes': 10234,
                'text': 'Однажды Лунтик решил отправиться в путешествие и выбрал для этого город Кострому. Он был очень любопытен и хотел узнать больше о культуре и истории этого города.'
            },
            {
                'name': 'Лунтик у Илона Маска',
                'likes': 12223,
                'text': 'Когда Лунтик прибыл в дом Илона Маска, он был поражен технологическими достижениями, которые были созданы в этом доме. Илон Маск показал ему свои последние изобретения, такие как электрические автомобили и космические корабли.'
            }
        ]
    },
    {
        'name': 'Фанфики про Вупсеня',
        'fanfics': [
            {
                'name': 'Анжуманя. Дуров. Вупсень',
                'likes': 9981,
                'text': 'Павел Дуров был дружелюбен и заинтересован в идеях Вупсени. Они начали обсуждать различные проекты, которые могут улучшить социальную сеть. Вупсеня предложил создать новый инструмент для групповых чатов, который позволит пользователям создавать анжуманя - интерактивные голосования и опросы.'
            }
        ]
    }
]

def save_to_storage():
    with open('fanfics.json', 'w') as file:
        file.write(json.dumps(categories, ensure_ascii=False))

def load_to_storage():
    with open('fanfics.json', 'r') as file:
        return json.loads(file.read())

try:
    categories = load_to_storage()
except:
    pass

@app.route('/')
def homepage():
    return render_template('page_home.html', categories=categories)

@app.route('/category/<int:category_id>/')
def category_page(category_id):
    if category_id < 0 or category_id >= len(categories):
        abort(404)
    return render_template('page_category.html', category_id=category_id, topic=categories[category_id])

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/like')
def add_like(category_id, fanfic_id):

    categories[category_id]['fanfics'][fanfic_id]['likes'] += 1
    return redirect(f'/category/{category_id}')

@app.route('/category/<int:category_id>/add', methods=['GET'])
def create_new_funf(category_id):
    return render_template('page_addfunf.html', category_id=category_id)

@app.route('/category/<int:category_id>/add', methods=['POST'])
def create_new_fanfic(category_id):
    title = request.form['title']
    text = request.form['text']
    topic = categories[category_id]
    topic['fanfics'].append({
        'name': title,
        'text': text,
        'likes': 0
    })
    save_to_storage()
    return redirect(f'/category/{category_id}')

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/del')
def fanfic_delete(category_id, fanfic_id):
    del categories[category_id]['fanfics'][fanfic_id]
    save_to_storage()
    return redirect(f'/category/{category_id}')

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/edit', methods=['GET'])
def change_the_funf(category_id, fanfic_id):
    return render_template('page_editfunf.html', category_id=category_id, fanfic_id=fanfic_id, topic = categories[category_id]['fanfics'][fanfic_id])

@app.route('/category/<int:category_id>/fanfic/<int:fanfic_id>/edit', methods=['POST'])
def edit_funf(category_id, fanfic_id):
    title = request.form['title']
    text = request.form['text']
    topic = categories[category_id]['fanfics'][fanfic_id]
    topic['name'] = title
    topic['text'] = text
    save_to_storage()
    return redirect(f'/category/{category_id}')

@app.route('/addcat', methods=['GET'])
def create_new_cat():
    return render_template('page_addcat.html')

@app.route('/addcat', methods=['POST'])
def make_new_cat():
    title = request.form['title']
    categories.append({
        'name': title,
        'fanfics': []
    })
    save_to_storage()
    return redirect('/')

@app.route('/category/<int:category_id>/del')
def del_category(category_id):
    del categories[category_id]
    save_to_storage()
    return redirect('/')

@app.route('/category/<int:category_id>/edit', methods=['GET'])
def edit_cat(category_id):
    return render_template('page_editcat.html', categories=categories, category_id=category_id)

@app.route('/category/<int:category_id>/edit', methods=['POST'])
def edit_category(category_id):
    title = request.form['title']
    categories[category_id]['name'] = title
    save_to_storage()
    return redirect('/')

app.run(debug=True)