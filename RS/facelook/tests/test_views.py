from django.test import TestCase, Client
from django.urls import reverse
from facelook.models import *
import json, os, sys


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index = reverse('index')
        self.login = reverse('login_user')
        self.register = reverse('registe')
        self.profile = reverse('profile', args =  [1])
        self.edit_profile = reverse('edit_profile')
        self.topic = reverse('topic', args = [1])
        self.topics = reverse('topics')
        self.posts = reverse('posts', args = [1])
        self.post_add = reverse('add_post')



        
        self.user1_obj = User.objects.create( first_name='testuser', last_name='testuser', username='testuser', email = 'email@email.com', password = "password" )
        self.user2_obj = User.objects.create( first_name='testuser2', last_name='testuser2', username='testuser2', email = 'email2@email.com', password = "password2" )
        self.topic_obj = Topic.objects.create( title = 'test topic', text = 'test content', creator = self.user1_obj )
        self.post_obj = Post.objects.create( text = 'test post', topic = self.topic_obj, creator = self.user1_obj )
        self.like_obj = Like.objects.create( value = True, post = self.post_obj, user = self.user1_obj )
        self.fallowing_obj = Fallowing.objects.create( user = self.user1_obj, fallower = self.user2_obj )
        



        
    def test_index_GET(self):
        response = self.client.get(self.index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_index_POST(self):
        response = self.client.post(self.index)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_GET(self):
        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_POST(self):
        response = self.client.post(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    

    def test_register_GET(self):
        response = self.client.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_register_POST(self):
        response = self.client.post(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_topic_POST(self):
        response = self.client.post(self.topic)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'topic.html')
    
    def test_topic_GET(self):
        response = self.client.get(self.topic)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'topic.html')
    
    def test_topics_GET(self):
        response = self.client.get(self.topics)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics.html')
    
    def test_topics_POST(self):
        response = self.client.post(self.topics)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'topics.html')
    
    def test_profile_GET(self):
        response = self.client.get(self.profile)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_profile_POST(self):
        response = self.client.post(self.profile)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
    
    def test_posts_POST(self):
        response = self.client.post(self.posts)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
    
    def test_posts_GET(self):
        response = self.client.get(self.posts)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts.html')
    
    def test_post_add_POST(self):
        response = self.client.post(self.post_add, {
            'text': 'test post',
            'topic': self.topic_obj,
            'creator': self.user1_obj
        })
        self.assertEquals(response.status_code, 302)
    
    def test_topic_add_POST(self):
        response = self.client.post(self.topic, {
            'title': 'test topic',
            'text': 'test content',
            'creator': self.user1_obj
        })
        self.assertEquals(response.status_code, 200)
    
