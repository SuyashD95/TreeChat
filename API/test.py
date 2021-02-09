from datetime import datetime

import requests

from main import db, UserModel as User, RoomModel as Room, MessageModel as Message

LOCAL_DEV_SERVER = 'http://127.0.0.1:5000/'


def load_database():
    """Helper method used for pre-populating the test SQLite database
    with some initial data.
    """
    # Creating the tables in the database based on the Models
    db.create_all()
    print('Tables are successfully created in the database.', end='\n\n')

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
    print('Successfully inserted new records into the user table.')

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
    print('Successfully inserted new records into the room table.')

    sender_2 = db.session.query(User).filter_by(name='User 2').first()
    sender_3 = db.session.query(User).filter_by(name='User 3').first()

    room_1 = db.session.query(Room).filter_by(name='Room 1').first()
    room_2 = db.session.query(Room).filter_by(name='Room 2').first()

    messages_data = [
        {
            'body': 'Text for message 1 sent by User 2 in Room 1.',
            'timestamp': datetime.now(),
            'sender': sender_2,
            'room': room_1
        },
        {
            'body': 'Text for message 2 sent by User 1 in Room 1',
            'timestamp': datetime.now(),
            'sender': room_admin,
            'room': room_1
        },
        {
            'body': 'Text for message 3 sent by User 3 in Room 2',
            'timestamp': datetime.now(),
            'sender': sender_3,
            'room': room_2
        },
        {
            'body': 'Text for message 3 sent by User 2 in Room 2',
            'timestamp': datetime.now(),
            'sender': sender_2,
            'room': room_2
        }
    ]

    print('Inserting mock data to the message table in the database...')
    for message in messages_data:
        new_message = Message(body=message['body'], timestamp=message['timestamp'], room_id=message['room']._id)
        message['sender'].sends.append(new_message)
        db.session.commit()
        print(f'Added new message, "{new_message.body}", sent by {new_message.user.name} on {new_message.room.name}')
    print('Successfully inserted new records into the message table.')


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

    # Drop all the tables in the database
    db.drop_all()
    print('All the tables have been dropped from the database.')


if __name__ == '__main__':
    # Pre-pop1ulate data into the database
    load_database()

    # Deleting all existing in the database
    clean_database()
