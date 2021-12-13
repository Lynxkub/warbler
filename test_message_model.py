"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_add_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_delete_message(self):
        """Can we delete a message"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

        resp = c.post('/messages/new', data = {'text': 'Hello'})

        self.assertEqual(resp.status_code, 302)

        msg = Message.query.one()
        self.assertEqual(msg.text, "Hello")

        delete_resp = c.post('/messages/1/delete')

        
        msg = Message.query.get(1)
        self.assertTrue(msg == None)

    def test_like_message(self):
        """Can we like a message"""


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

      

        resp = c.post('/messages/new', data = {'text': 'Hello'})

        self.assertEqual(resp.status_code, 302)

        msg = Message.query.one()
        print('**********')
        print(msg.id)
        self.assertEqual(msg.text, "Hello")

        self.new_user = User.signup(
            username = 'new_user',
            email = 'test1@test.com',
            password = 'HASHED_PASSWORD',
            image_url=None

        )

        with self.client as d:
            with d.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.new_user.id

        d.post('/users/add_like/3')
        
        # self.assertEqual(r.status_code, 302)
        self.assertNotIn('3',self.new_user.likes)


        # test_message = self.new_user.post('/message/new', data = {'text':'Hi'})

