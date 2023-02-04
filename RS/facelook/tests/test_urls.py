from django.test import SimpleTestCase
from django.urls import reverse, resolve
from facelook.views import *

class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index)
    
    def test_user_list_url_is_resolved(self):
        url = reverse('users_list')
        self.assertEquals(resolve(url).func, users_list)

    def test_login_user_url_is_resolved(self):
        url = reverse('login_user')
        self.assertEquals(resolve(url).func, login_user)

    def test_registe_url_is_resolved(self):
        url = reverse('registe')
        self.assertEquals(resolve(url).func, registe)

    def test_logout_user_url_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_user)

    def test_edit_profile_url_is_resolved(self):
        url = reverse('edit_profile')
        self.assertEquals(resolve(url).func, edit_profile)

    def test_topics_url_is_resolved(self):
        url = reverse('topics')
        self.assertEquals(resolve(url).func, topics)

    def test_add_post_url_is_resolved(self):
        url = reverse('add_post')
        self.assertEquals(resolve(url).func, add_post)

    def test_add_topic_url_is_resolved(self):
        url = reverse('add_topic')
        self.assertEquals(resolve(url).func, add_topic)

    def test_password_edit_url_is_resolved(self):
        url = reverse('password_edit')
        self.assertEquals(resolve(url).func, password_edit)

    def test_profile_url_is_resolved(self):
        url = reverse('profile', args=[1])
        self.assertEquals(resolve(url).func, profile)

    def test_topic_url_is_resolved(self):
        url = reverse('topic', args=[1])
        self.assertEquals(resolve(url).func, topic)

    def test_posts_url_is_resolved(self):
        url = reverse('posts', args=[1])
        self.assertEquals(resolve(url).func, posts)

    def test_edit_post_url_is_resolved(self):
        url = reverse('edit_post', args=[1])
        self.assertEquals(resolve(url).func, edit_post)

    def test_posts_for_user_url_is_resolved(self):
        url = reverse('posts_for_user', args=[1])
        self.assertEquals(resolve(url).func, posts_for_user)

    def test_topics_for_user_url_is_resolved(self):
        url = reverse('topics_for_user', args=[1])
        self.assertEquals(resolve(url).func, topics_for_user)
        
    def test_follow_or_unfollow_url_is_resolved(self):
        url = reverse('follow_or_unfollow', args=[1])
        self.assertEquals(resolve(url).func, follow_or_unfollow)
        
    def test_delete_url_is_resolved(self):
        url = reverse('delete', args=[1, 'post'])
        self.assertEquals(resolve(url).func, delete)
    def test_delete_url_is_resolved(self):
        url = reverse('delete', args=[1, 'topic'])
        self.assertEquals(resolve(url).func, delete)