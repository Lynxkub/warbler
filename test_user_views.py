import os
from unittest import TestCase

from models import db,connect_db, User, Message, Follows, Likes


os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import CURR_USER_KEY, app, do_login




class UserTestViewsTestCase(TestCase):
    """Test view functions for user"""
    def setup(self):
        """Create a test client"""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        self.u1 = User.signup('abc', 'test1@test1.com', 'password', None)
        self.u1_id = 100
        self.u1.id = self.u1_id
        self.u2 = User.signup('efg', 'test2@test.com', 'password', None)
        self.u2_id = 200
        self.u2.id = self.u2_id
        
        db.session.commit()
    
    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp
        

    def test_home_page(self):
        """Test home page"""

        with app.test_client() as client:
            resp = client.get('/')
            
            self.assertEqual(resp.status_code, 200)
            
    def test_anon_home_page(self):
        """Test non logged in user homepage"""

        User.query.delete()
        db.session.commit()

        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/signup" class="btn btn-primary">Sign up</a>', html)


   
      




