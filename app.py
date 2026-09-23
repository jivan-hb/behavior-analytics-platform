from models import User

from flask import Flask, request, abort
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

def validate_text(value):
    return isinstance(value, str) and value.strip()


def validate_age(age):
    return type(age) is int and age > 0

def validate_user(name, surname, age):
    return validate_text(name) and validate_text(surname) and validate_age(age)

def get_user_by_id(id):
    user = User.select().where(User.id == id).first()
    if user:
        return user
    abort(404)


def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age
    }

@app.errorhandler(HTTPException)
def error_handler(error):
    return {
        "error": error.name
    }, error.code

@app.route('/search')
def search():
    search_query = request.args.get('q')

    if search_query:
        return f"Вы искали: {search_query}"
    return "Поисковый запрос не задан."



@app.route('/message', methods=['POST'])
def message():
    query = request.get_json()
    return query.get('hello')


@app.route('/users', methods=['POST'])
def users_post():
    query = request.get_json(silent=True)
    if query:
        name = query.get('name')
        surname = query.get('surname')
        age = query.get('age')

        if validate_user(name, surname, age):
            user = User.create(name=name.strip(), surname=surname.strip(), age=age)
            return user_to_dict(user), 201
    abort(400)


@app.route('/users')
def users_list():
    search = request.args.get('search')

    if search:
        users_query = User.select().where(
            User.name.contains(search) |
            (User.surname.contains(search))
        )
    else:
        users_query = User.select()

    users = []

    for user in users_query:
        users.append(user_to_dict(user))


    return users, 200


@app.route('/users/<int:id>')
def get_user_info(id):
    user = get_user_by_id(id)
    return user_to_dict(user), 200




@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = get_user_by_id(id)

    username = user.name
    user_id = user.id

    User.delete().where(User.id == id).execute()
    return {
        "message": f'Пользователь {username} успешно удален',
        "id": user_id
    }, 200


@app.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    user = get_user_by_id(id)
    changed = False

    query = request.get_json(silent=True)
    if query:
        name = query.get('name')
        surname = query.get('surname')
        age = query.get('age')

        if validate_text(name):
            user.name = name.strip()
            changed = True

        if validate_text(surname):
            user.surname = surname.strip()
            changed = True

        if validate_age(age):
            user.age = age
            changed = True

        if changed:
            user.save()
            return user_to_dict(user), 200
    abort(400)




if __name__ == '__main__':
    app.run(debug=True)