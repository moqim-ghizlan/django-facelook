from django.test import SimpleTestCase
from facelook.forms import NewUserForm, TopicForm, PostForm
from facelook.models import User, Post, Topic, Like, Fallowing



class TestForms(SimpleTestCase):
    databases = '__all__' # To let the test use the db

    def test_user_form_valid_data(self):
        
        form = NewUserForm(data={
            'first_name': 'first_name',
            'last_name': 'last_name',
            'username' : 'username',
            'email': 'email@email.email',
            'password1': 'Password12345++',
            'password2' : 'Password12345++'
            })
        self.assertTrue(form.is_valid())
    
    def test_user_form_no_data(self):        

        form = NewUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 6)

    def test_topic_form_valid_data(self):
        form = TopicForm(data={
            'title': 'title',
            'text': 'text',
            })
        self.assertTrue(form.is_valid())
    
    def test_topic_form_no_data(self):
        form = TopicForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
    
    def test_post_form_valid_data(self):
        form = PostForm(data={
            'text': 'text',
            })
        self.assertTrue(form.is_valid() != True) #Because we need a topic to create the post :)
    
    def test_post_form_no_data(self):
        form = PostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)