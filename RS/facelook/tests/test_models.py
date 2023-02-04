from django.test import TestCase
from facelook.models import *

class TestModels(TestCase):
    def setUp(self):
        self.user1_obj = User.objects.create( first_name='testuser', last_name='testuser', username='testuser1', email = 'email1@email.com', password = "password" )
        self.user2_obj = User.objects.create( first_name='testuser2', last_name='testuser2', username='testuser2', email = 'email2@email.com', password = "password" )
        self.topic1_obj = Topic.objects.create( title = 'title', text = 'text', creator = self.user1_obj )
        self.post1_obj = Post.objects.create( text = 'text', topic = self.topic1_obj, creator = self.user1_obj )
        self.like1_obj = Like.objects.create( value = True, post = self.post1_obj, user = self.user1_obj )
        self.fallowing1_obj = Fallowing.objects.create( user = self.user1_obj, fallower = self.user2_obj )
        
    def test_user_info_on_creation(self):
        self.assertEqual(self.user1_obj.first_name, "testuser")
        self.assertEqual(self.user1_obj.last_name, "testuser")
        self.assertEqual(self.user1_obj.username, "testuser1")
        self.assertEqual(self.user1_obj.email, "email1@email.com")
        self.assertEqual(self.user1_obj.password, "password")
    
    def test_topic_info_on_creation(self):
        self.assertEqual(self.topic1_obj.title, "title")
        self.assertEqual(self.topic1_obj.text, "text")
        self.assertEqual(self.topic1_obj.creator, self.user1_obj)
    
    def test_post_info_on_creation(self):
        self.assertEqual(self.post1_obj.text, "text")
        self.assertEqual(self.post1_obj.topic, self.topic1_obj)
        self.assertEqual(self.post1_obj.creator, self.user1_obj)
    
    def test_like_info_on_creation(self):
        self.assertEqual(self.like1_obj.value, True)
        self.assertEqual(self.like1_obj.post, self.post1_obj)
        self.assertEqual(self.like1_obj.user, self.user1_obj)
    
    def test_fallowing_info_on_creation(self):
        self.assertEqual(self.fallowing1_obj.user, self.user1_obj)
        self.assertEqual(self.fallowing1_obj.fallower, self.user2_obj)
    
    def test_user_info_on_update(self):
        self.user1_obj.first_name = "new_firstname"
        self.user1_obj.last_name = "new_lastname"
        self.user1_obj.username = "new_username"
        self.user1_obj.email = "new_email@email.com"
        self.user1_obj.password = "new_password"
        self.user1_obj.save()
        self.assertEqual(self.user1_obj.first_name, "new_firstname")
        self.assertEqual(self.user1_obj.last_name, "new_lastname")
        self.assertEqual(self.user1_obj.username, "new_username")
        self.assertEqual(self.user1_obj.email, "new_email@email.com")
        self.assertEqual(self.user1_obj.password, "new_password")
    
    def test_topic_info_on_update(self):
        self.topic1_obj.title = "new_title"
        self.topic1_obj.text = "new_text"
        self.topic1_obj.creator = self.user2_obj
        self.topic1_obj.save()
        self.assertEqual(self.topic1_obj.title, "new_title")
        self.assertEqual(self.topic1_obj.text, "new_text")
        self.assertEqual(self.topic1_obj.creator, self.user2_obj)
    
    def test_post_info_on_update(self):
        self.post1_obj.text = "new_text"
        self.post1_obj.topic = self.topic1_obj
        self.post1_obj.creator = self.user2_obj
        self.post1_obj.save()
        self.assertEqual(self.post1_obj.text, "new_text")
        self.assertEqual(self.post1_obj.topic, self.topic1_obj)
        self.assertEqual(self.post1_obj.creator, self.user2_obj)

    def test_like_info_on_update(self):
        self.like1_obj.value = False
        self.like1_obj.post = self.post1_obj
        self.like1_obj.user = self.user2_obj
        self.like1_obj.save()
        self.assertEqual(self.like1_obj.value, False)
        self.assertEqual(self.like1_obj.post, self.post1_obj)
        self.assertEqual(self.like1_obj.user, self.user2_obj)
    
    def test_fallowing_info_on_update(self):
        self.fallowing1_obj.user = self.user2_obj
        self.fallowing1_obj.fallower = self.user1_obj
        self.fallowing1_obj.save()
        self.assertEqual(self.fallowing1_obj.user, self.user2_obj)
        self.assertEqual(self.fallowing1_obj.fallower, self.user1_obj)
        
    def test_user_info_on_delete(self):
        self.user1_obj.delete()
        self.assertEqual(User.objects.count(), 1)
        
    def test_topic_info_on_delete(self):
        self.topic1_obj.delete()
        self.assertEqual(Topic.objects.count(), 0)
    
    def test_post_info_on_delete(self):
        self.post1_obj.delete()
        self.assertEqual(Post.objects.count(), 0)
    
    def test_like_info_on_delete(self):
        self.like1_obj.delete()
        self.assertEqual(Like.objects.count(), 0)
    
    def test_fallowing_info_on_delete(self):
        self.fallowing1_obj.delete()
        self.assertEqual(Fallowing.objects.count(), 0)
    
    def test_user_info_on_get(self):
        self.assertEqual(User.objects.get(id = 1), self.user1_obj)
        self.assertEqual(User.objects.get(id = 2), self.user2_obj)
    
    def test_topic_info_on_get(self):
        self.assertEqual(Topic.objects.get(id = 1), self.topic1_obj)
    
    def test_post_info_on_get(self):
        self.assertEqual(Post.objects.get(id = 1), self.post1_obj)
    
    def test_like_info_on_get(self):
        self.assertEqual(Like.objects.get(id = 1), self.like1_obj)
    
    def test_fallowing_info_on_get(self):
        self.assertEqual(Fallowing.objects.get(id = 1), self.fallowing1_obj)
    
    def test_user_info_on_get_all(self):
        self.assertEqual(User.objects.all().count(), 2)
    
    def test_topic_info_on_get_all(self):
        self.assertEqual(Topic.objects.all().count(), 1)

    def test_post_info_on_get_all(self):
        self.assertEqual(Post.objects.all().count(), 1)

    def test_like_info_on_get_all(self):
        self.assertEqual(Like.objects.all().count(), 1)

    def test_fallowing_info_on_get_all(self):
        self.assertEqual(Fallowing.objects.all().count(), 1)

