from models import User

def validate_text(value):
    return isinstance(value, str) and bool(value.strip())

def validate_age(age):
    return type(age) is int and age > 0

def validate_user(name, surname, age):
    return validate_text(name) and validate_text(surname) and validate_age(age)

def get_user_by_id(id):
    return User.select().where(User.id == id).first()

def user_to_dict(user):
    return {
        'id': user.id,
        'name': user.name,
        'surname': user.surname,
        'age': user.age
    }

def create_user(name, surname, age):

    if validate_user(name, surname, age):
        user = User.create(name=name.strip(),
                           surname=surname.strip(),
                           age=age
                        )
        return user

    return False

def get_users(search):

    if search:
        users_query = User.select().where(
            User.name.contains(search) |
            User.surname.contains(search)
        )
        return users_query
    return User.select()

def delete_user(id):

    user = get_user_by_id(id)

    if user:

        name = user.name
        user_id = user.id
        User.delete().where(User.id == id).execute()

        return name, user_id

    return None


def validate_update(query):
    if not query:
        return False

    allowed_fields = {'name', 'surname', 'age'}

    if not all(key in allowed_fields for key in query):
        return False

    if 'name' in query and not validate_text(query['name']):
        return False

    if 'surname' in query and not validate_text(query['surname']):
        return False

    if 'age' in query and not validate_age(query['age']):
        return False

    return True


def update_user(id, query):
    if not validate_update(query):
        return False

    user = get_user_by_id(id)

    if not user:
        return None

    if 'name' in query:
        user.name = query['name'].strip()

    if 'surname' in query:
        user.surname = query['surname'].strip()

    if 'age' in query:
        user.age = query['age']

    user.save()
    return user
