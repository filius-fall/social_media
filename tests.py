from datetime import datetime,timedelta
import unittest

from werkzeug.security import check_password_hash
from app import db,app
from app.models import User,Post

class UserModelCase(unittest.TestCase):
    def setup(self):
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password(self):
        u=User(username='filius',email='filius@example.com')
        u.set_password('fall')
        self.assertFalse(u.check_password('fill'))
        self.assertTrue(u.check_password('fall'))
    
    # def avatar_test(self):
    #     v=User(username='rams',email='rams@example.com')
    #     self.assertEqual(v.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      'd4c74594d841139328695756648b6bd6'
    #                                      '?d=identicon&s=128'))

    def follow_test(self):
        w=User(username='filiusfall',email='filiusfall@example.com')
        x=User(username='rams',email='rams@exmaple.com')
        db.session.add(w)
        db.session.add(x)
        db.session.commit()
        self.assertEqual(w.followers.all(),[])
        self.assertEqual(x.followed.all(),[])


        w.follow(x)
        db.session.commit()
        self.assertTrue(w.is_following(x))
        self.assertEqual(w.followed.count(),1)
        self.assertEqual(w.followed.first().username,'rams')
        self.assertEqual(x.followers.count(),1)
        self.assertEqual(x.follwers.first().username,'filiusfall')

        w.unfollow(x)
        db.session.commit()
        self.assertFalse(w.is_following(x))
        self.assertEqual(w.followed.count(),0)
        self.assertEqual(x.followers.count(),0)

if __name__ == '__main__':
    unittest.main(verbosity=2)