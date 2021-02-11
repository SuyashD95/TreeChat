from datetime import datetime
from json import dumps as json_dumps
from sqlalchemy import exc

import requests

from main import db, UserModel as User, RoomModel as Room, MessageModel as Message

LOCAL_DEV_SERVER = 'http://127.0.0.1:5000/'

# A lambda function to format JSON responses in more human-readable manner
prettify_json = lambda json_response, indent=2: json_dumps(json_response, indent=indent)


def load_database():
    """Helper method used for pre-populating the test SQLite database
    with some initial data.
    """
    users_data = [
        {
            'name': 'User 1',
            'email': 'user1@email.com',
            'password': 'User1_Password'
        },
        {
            'name': 'User 2',
            'email': 'user2@email.com',
            'password': 'User2_Password'
        },
        {
            'name': 'User 3',
            'email': 'user3@email.com',
            'password': 'User3_Password'
        }
    ]

    print('Inserting mock data to the user table in the database...')
    for user in users_data:
        new_user = User(name=user['name'], email=user['email'], password=user['password'])
        db.session.add(new_user)
        db.session.commit()
        print(f'Added {new_user.name} into the database.')
    print('Successfully inserted new records into the user table.', end='\n\n')

    room_admin = db.session.query(User).filter_by(name='User 1').first()
    
    rooms_data = [
        {'name': 'Room 1'},
        {'name': 'Room 2'}
    ]

    print('Inserting mock data to the room table in the database...')
    for room in rooms_data:
        new_room = Room(name=room['name'])
        room_admin.is_admin.append(new_room)
        db.session.commit()
        print(f'Added {new_room.name} into the database w/ {new_room.user.name} as its admin.')
    print('Successfully inserted new records into the room table.', end='\n\n')

    sender_2 = db.session.query(User).filter_by(name='User 2').first()
    sender_3 = db.session.query(User).filter_by(name='User 3').first()

    room_1 = db.session.query(Room).filter_by(name='Room 1').first()
    room_2 = db.session.query(Room).filter_by(name='Room 2').first()

    messages_data = [
        {
            'body': 'Text for message 1 sent by User 2 in Room 1.',
            'sender': sender_2,
            'room': room_1
        },
        {
            'body': 'Text for message 2 sent by User 1 in Room 1',
            'sender': room_admin,
            'room': room_1
        },
        {
            'body': 'Text for message 3 sent by User 3 in Room 2',
            'sender': sender_3,
            'room': room_2
        },
        {
            'body': 'Text for message 3 sent by User 2 in Room 2',
            'sender': sender_2,
            'room': room_2
        }
    ]

    print('Inserting mock data to the message table in the database...')
    for message in messages_data:
        new_message = Message(body=message['body'], room_id=message['room']._id)
        message['sender'].sends.append(new_message)
        db.session.commit()
        print(f'Added new message, "{new_message.body}", sent by {new_message.user.name} on {new_message.room.name}')
    print('Successfully inserted new records into the message table.', end='\n')
    input('Press any key to continue...\n')


def test_get_all_users(base_url, expected_success_code=200, expected_fail_code=404):
    """An unit test to ensure that the endpoint to get all the existing
    users is working properly.
    """
    ENDPOINT = 'users/all'
    response = requests.get(f'{base_url}{ENDPOINT}')

    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    input('Press any key to continue...\n')


def test_get_user_by_name(base_url, name, expected_success_code=200, expected_fail_code=404):
    """An unit test to ensure that the endpoint to get an user by name
    is working properly.
    """
    ENDPOINT = f'users/{name}'
    response = requests.get(f'{base_url}{ENDPOINT}')

    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    input('Press any key to continue...\n')


def test_create_user(base_url, names, expected_success_code=201, expected_fail_code=409):
    """An unit test to ensure that the endpoint to create a new user by name
    is working properly.
    """
    ENDPOINT = f'users/new'

    valid_request_bodies = [
        {
            'name': names[0],
            'password': 'pass@123',
            'email': f'{names[0]}@email.com'
        },
        {
        'name': names[1],
        'password': 'pwd@abc'
        }
    ]

    for body in valid_request_bodies:
        response = requests.post(f'{base_url}{ENDPOINT}', data=body)
        if response.status_code == expected_success_code:
            print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
        elif response.status_code == expected_fail_code:
            print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
        else:
            print(
                f'Some unexpected error has occurred. '
                f'Returned response code: {response.status_code}'
            )
        print()
    input('Press any key to continue...\n')

    expected_success_code = 409
    expected_fail_code = 201
    
    faulty_request_bodies = [
        {
            'name': 'User 1',
            'password': 'pwd2020'
        },
        {
            'name': 'Don\'t Care',
            'password': ''
        },
        {
            'nam5': 'Invalid Parameter'
        },
        {
            'name': 'Valid Name Param',
            'email': 'Valid Email Param'
        },
        {
            'name': 'Valid',
            'password': 'Valid',
            'ema1L': 'Invalid'
        }
    ]

    for body in faulty_request_bodies:
        response = requests.post(f'{base_url}{ENDPOINT}', json=body)
        if response.status_code == expected_success_code:
            print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
        elif response.status_code == expected_fail_code:
            print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
        else:
            print(
                f'Some unexpected error has occurred. '
                f'Returned response code: {response.status_code}'
            )
            try:
                print(f'JSON:\n{response.json()}')
            except ValueError :
                print('No additional data was returned.')
        print()
    input('Press any key to continue...\n')
    

def test_get_all_rooms(base_url, expected_success_code=200, expected_fail_code=404):
    """An unit test to ensure that the endpoint to get all the existing
    rooms is working properly.
    """
    ENDPOINT = 'rooms/all'
    response = requests.get(f'{base_url}{ENDPOINT}')

    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    input('Press any key to continue...\n')


def test_get_room_by_name(base_url, name, expected_success_code=200, expected_fail_code=404):
    """An unit test to ensure that the endpoint to get a room by name
    is working properly.
    """
    ENDPOINT = f'rooms/{name}'
    response = requests.get(f'{base_url}{ENDPOINT}')

    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    input('Press any key to continue...\n')


def test_create_room(base_url, room_name, expected_success_code=201, expected_fail_code=409):
    """An unit test to ensure that the endpoint to create a new rooms by name
    is working properly.
    """
    ENDPOINT = f'rooms/new'

    valid_request_body = {
        'name': room_name,
        'room_admin_name': 'User 2'
    }

    response = requests.post(f'{base_url}{ENDPOINT}', json=valid_request_body)
    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    print()
    input('Press any key to continue...\n')

    expected_success_code = 409
    expected_fail_code = 201
    
    faulty_request_bodies = [
        {
            'name': 'Room 1',
            'room_admin_name': 'User 2'
        },
        {
            'name': 'Room 5',
            'room_admin_name': 'I don\'t exist'
        },
        {
            'name': 'Valid Name of Room'
        },
        {
            'room_admin_name': 'Valid Name of Admin'
        },
        {
            'name': 'Valid Room 1',
            'r00m_Admin_Name': 'User 3'
        }
    ]

    for body in faulty_request_bodies:
        response = requests.post(f'{base_url}{ENDPOINT}', json=body)
        if response.status_code == expected_success_code:
            print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
        elif response.status_code == expected_fail_code:
            print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
        else:
            print(
                f'Some unexpected error has occurred. '
                f'Returned response code: {response.status_code}'
            )
            try:
                print(f'JSON:\n{response.json()}')
            except ValueError :
                print('No additional data was returned.')
        print()
    input('Press any key to continue...\n')


def test_get_all_msgs_of_a_room(base_url, room_name, expected_success_code=200, expected_fail_code=404):
    """An unit test to ensure that the endpoint to get all messages by
    the given room name is working properly.
    """
    ENDPOINT = f'messages/{room_name}'
    response = requests.get(f'{base_url}{ENDPOINT}')

    if response.status_code == expected_success_code:
        print(f'Result: SUCCESS.\nJSON:\n{prettify_json(response.json())}')
    elif response.status_code == expected_fail_code:
        print(f'Result: FAILED.\nJSON:\n{prettify_json(response.json())}')
    else:
        print(
            f'Some unexpected error has occurred. '
            f'Returned response code: {response.status_code}'
        )
    input('Press any key to continue...\n')


def clean_database():
    """A helper method to delete all existing data stored in the local
    database.
    """
    print('Deleting all the data stored in the tables in the database...')
    
    message_deleted_row_count = db.session.query(Message).delete()
    if message_deleted_row_count:
        print('Successfully delete all the the data in the message table.')
    else:
        print('Failed to delete all the data in the message table.')
    
    room_deleted_row_count = db.session.query(Room).delete()
    if room_deleted_row_count:
        print('Successfully delete all the the data in the room table.')
    else:
        print('Failed to delete all the data in the room table.')

    user_deleted_row_count = db.session.query(User).delete()
    if user_deleted_row_count:
        print('Successfully delete all the the data in the user table.')
    else:
        print('Failed to delete all the data in the user table.')
    
    db.session.commit()
    print('Successfully deleted all the data in the database.', end='\n\n')


if __name__ == '__main__':
    # Creating the tables in the database based on the Models
    db.create_all()
    print('Tables are successfully created in the database.', end='\n\n')
    input('Press any key to continue...\n')

    # Pre-populate data into the database
    try:
        load_database()
    except exc.SQLAlchemyError as sql_alchemy_err:
        print(f'\nSQLAlchemy Error:\n{sql_alchemy_err}\n')
        print(f'Rolling back all the transactions in the current session...')
        db.session.rollback()
        input('Press any key to continue...\n')

    # Run unit tests
    # --------------
    # Testing /users/all
    test_get_all_users(LOCAL_DEV_SERVER)
    # Testing /user/{name}
    test_get_user_by_name(LOCAL_DEV_SERVER, 'User 2')
    test_get_user_by_name(LOCAL_DEV_SERVER, 'Unknown User', expected_success_code=404, expected_fail_code=200)
    # Testing /users/new
    test_create_user(LOCAL_DEV_SERVER, ['User 4', 'User 5'])
    # Testing /rooms/all
    test_get_all_rooms(LOCAL_DEV_SERVER)
    # Testing /rooms/{name}
    test_get_room_by_name(LOCAL_DEV_SERVER, 'Room 2')
    test_get_room_by_name(LOCAL_DEV_SERVER, 'Unknown Room', expected_success_code=404, expected_fail_code=200)
    # Testing /rooms/new
    test_create_room(LOCAL_DEV_SERVER, 'Room 3')
    # Testing /messages/{room_name}
    test_get_all_msgs_of_a_room(LOCAL_DEV_SERVER, 'Room 1')
    test_get_all_msgs_of_a_room(LOCAL_DEV_SERVER, 'Non-Existent Room', expected_success_code=404, expected_fail_code=200)
    test_get_all_msgs_of_a_room(LOCAL_DEV_SERVER, 'Room 3', expected_success_code=404, expected_fail_code=200)
    # --------------
    
    # Deleting all existing in the database
    clean_database()

    # Drop all the tables in the database
    db.drop_all()
    print('All the tables have been dropped from the database.')
