from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

from rest_framework import status
from .models import *

from .model_factories import *

# Create your tests here.

class AccountsTest(APITestCase):
    test_area = None
    def setUp(self):
        self.test_area = AreaFactory.create()
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        # URL for creating an account.
        # self.create_getArea_url = reverse('getArea')

    def tearDown(self):
        Area.objects.all().delete()

    ####################### TEST GET AREA API ##########################

    # test for valid get_area url
    def test_getArea_url(self):
        url = reverse('getArea', kwargs = {'areaName': 'manor park'})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        # test is has 1 area sent to client 
        self.assertEqual(len(response.data['areas']), 1)

    # test for invalid number areaName input
    def test_invalid_area_getArea_url(self):
        url = reverse('getArea', kwargs = {'areaName': 9})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 400) 

    ####################### TEST CREATE AREA API ##########################
    
    # test for createArea url
    def test_createArea_url(self):
        data = {
            'name': 'forest gate' ,
            'country': 'united kingdom',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], False)
        self.assertEqual(response.data['area_exists'], False)
        # area with name 'manor park' and id 1, created using factory. so this one would be id 2.
        self.assertEqual(response.data['area_id'], 2)

    # test for createArea url -> duplicate area name
    def test_createArea_url_duplicate_area_name(self):
        data = {
            'name': 'manor park' ,
            'country': 'united kingdom',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 409)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], False)
        self.assertEqual(response.data['area_exists'], True)
        self.assertEqual(response.data['area_id'], {'id':1})

    # test createArea with duplicate area name but different country
    def test_createArea_url_duplicate_area_name_with_different_country(self):
        data = {
            'name': 'manor park' ,
            'country': 'united states',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 201)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], False)
        self.assertEqual(response.data['area_exists'], False)
        # area with name 'manor park' and id 1, created using factory. so this one would be id 2.
        self.assertEqual(response.data['area_id'], 2)

    # test area form errors
    def test_createArea_url_no_name_input(self):
        data = {
            'name': '' ,
            'country': 'united kingdom',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], True)
        self.assertEqual(response.data['area_exists'], False)
        self.assertEqual(len(response.data['area_form_errors']), 1)

    # test area form short name error
    def test_createArea_url_short_name_input(self):
        data = {
            'name': 'm' ,
            'country': 'united kingdom',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], True)
        self.assertEqual(response.data['area_exists'], False)
        self.assertEqual(len(response.data['area_form_errors']), 1)

    # test area form short country error
    def test_createArea_url_short_country_input(self):
        data = {
            'name': 'derry' ,
            'country': 'un',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], True)
        self.assertEqual(response.data['area_exists'], False)
        self.assertEqual(len(response.data['area_form_errors']), 1)

    # test area form empty country input error
    def test_createArea_url_no_country_input(self):
        data = {
            'name': 'derry' ,
            'country': '',
            'city': 'london',
            'borough': 'newham'
           
        }
        createArea_url = reverse('createArea')
        response = self.client.post(createArea_url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
        # test is has 1 area sent to client 
        self.assertEqual(response.data['validation_errors'], True)
        self.assertEqual(response.data['area_exists'], False)
        self.assertEqual(len(response.data['area_form_errors']), 1)

    # edit these so that we're actually asserting what the errors say?

    #################### TEST SUBMIT DESCRIPTION API ############################

    # test submitDescription url
    def test_submitDescription_url(self):
        data = {
            'description': 'this is the best area ever!' ,
            'area_id': 1,
            'user': {'user_id': 1},
           
        }
        submitDescription_url = reverse('submitDescription')
        response = self.client.post(submitDescription_url, data, format='json')
        
        self.assertEqual(response.status_code, 201)

    # test submitDescription url
    def test_submitDescription_url_no_description(self):
        data = {
            'description': '' ,
            'area_id': 1,
            'user': {'user_id': 1},
           
        }
        submitDescription_url = reverse('submitDescription')
        response = self.client.post(submitDescription_url, data, format='json')
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data['errors']), 1)

    ####################### TEST SUBMIT FORM API ##########################
    
    # test submitForm url
    def test_submitForm_url(self):
        data = {
            'rating': 'litter_count' ,
            'id': 1,
           
        }
        submitForm_url = reverse('submitForm')
        response = self.client.post(submitForm_url, data, format='json')
        self.assertEqual(response.status_code, 201)


  

