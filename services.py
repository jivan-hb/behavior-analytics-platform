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

def update_user(id, query):
    user = get_user_by_id(id)
    changed = False

    if not user:
        return None

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
        return user

    return False
