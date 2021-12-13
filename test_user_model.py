"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

       


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_user_follows(self):
        """Does User Follows accumulate followers """
        test_user = User(
            email = 'test1@test.com',
            username = 'test1',
            password = 'HASHED_PASSWORD'
        )

        db.session.add(test_user)
        db.session.commit()

        test_user_2 = User(
            email = 'test2@test.com', 
            username = 'test2',
            password = 'HASHED_PASSWORD'
        )
        db.session.add(test_user_2)
        db.session.commit()

        self.assertNotIn(test_user_2, test_user.following)

        test_user.following.append(test_user_2)
       

        self.assertEqual(len(test_user.following), 1)
        self.assertIn(test_user_2, test_user.following)
        self.assertIn(test_user, test_user_2.followers)

    def test_invalid_user_credentials(self):
        """Does the model require correct values to create a new user"""

        new_user = User(
            email = 'asdfa',
            username = 'new_user',
            password = 'HASHED_PASSWORD'
        )
        db.session.add(new_user)
        db.session.commit()

        self.assertNotEqual(new_user.id, 1)


    def test_authenticate(self):
        """Does authentication work"""

        test_user_3 = User(
            email = 'test@test3.com',
            username = 'user_3',
            password = 'HASHED_PASSWORD'
        )

     
        
        User.signup(test_user_3.username, test_user_3.email, test_user_3.password, test_user_3.image_url)

        
        user = User.authenticate(test_user_3.username, test_user_3.password)

        self.assertTrue(user)

        user = User.authenticate(test_user_3.username, 'abc')
        self.assertFalse(user)

        user = User.authenticate('abc', test_user_3.password)
        self.assertFalse(user)

     