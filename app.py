
from flask import Flask, request, abort
from peewee import PeeweeException
from werkzeug.exceptions import HTTPException

from services import (
    get_user_by_id,
    user_to_dict,
    create_user,
    get_users,
    delete_user as delete_user_service,
    update_user
)

app = Flask(__name__)


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

        user = create_user(name, surname, age)

        if user:
            return user_to_dict(user), 201

        if user is None:
            abort(500)

    abort(400)




@app.route('/users')
def users_list():
    search = request.args.get('search')

    users_query = get_users(search)

    users = []

    for user in users_query:
        users.append(user_to_dict(user))


    return users, 200


@app.route('/users/<int:id>')
def get_user_info(id):
    user = get_user_by_id(id)
    if user:
        return user_to_dict(user), 200
    abort(404)




@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    result = delete_user_service(id)

    if not result:
        abort(404)

    username, user_id = result

    return {
        "message": f'Пользователь {username} успешно удален',
        "id": user_id
    }, 200



@app.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    query = request.get_json(silent=True)

    if not query:
        abort(400)

    try:
        user = update_user(id, query)
    except PeeweeException:
        abort(500)

    if user is None:
        abort(404)

    if user is False:
        abort(400)

    return user_to_dict(user), 200



if __name__ == '__main__':
    app.run(debug=True)