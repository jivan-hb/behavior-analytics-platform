from models import User

if isinstance(name, str) and name.strip():
    name = name.strip()
    user.name = name
    changed = True

if isinstance(surname, str) and surname.strip():
    surname = surname.strip()
    user.surname = surname
    changed = True

if isinstance(age, int) and age > 0:
    user.age = age
    changed = True


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
    abort(400)


def validate_text(value):
    return isinstance(value, str) and value.strip()


def validate_age(age):
    return type(age) is int and age > 0

def validate_text(value):
    return isinstance(value, str) and value.strip()


def validate_age(age):
    return type(age) is int and age > 0

def validate_user(name, surname, age):
    if validate_text(name) and validate_text(surname) and validate_age(age):
        return True
    return False

def validate_user(name, surname, age):
    return validate_text(name) and validate_text(surname) and validate_age(age)