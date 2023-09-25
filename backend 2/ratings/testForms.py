import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .forms import *

# test forms
class FormTest(APITestCase):

######################### TEST AREA FORM ###############################

    # test AreaForm ideal form input
    def test_AreaForm_ideal_input(self):
        form_data = {'name': 'something', 'city': 'something else', 'country': 'something extra', 'borough': 'something better'}
        areaForm = AreaForm(form_data)
        self.assertTrue(areaForm.is_valid())
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 0)

    # test AreaForm form only name input
    def test_AreaForm_only_name(self):
        form_data = {'name': 'something'}
        areaForm = AreaForm(form_data)
        self.assertFalse(areaForm.is_valid())
       
        self.assertFormError(areaForm, 'city', 'This field is required.')
        self.assertFormError(areaForm, 'country', 'This field is required.')
        self.assertFormError(areaForm, 'borough', 'This field is required.')
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 3)

    # test AreaForm form only name input
    def test_AreaForm_name_missing(self):
        form_data = {'city': 'something else', 'country': 'something extra', 'borough': 'something better'}
        areaForm = AreaForm(form_data)
        self.assertFalse(areaForm.is_valid())
       
        self.assertFormError(areaForm, 'name', 'This field is required.')
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 1)

    # test AreaForm form country missing
    def test_AreaForm_country_missing(self):
        form_data = {'city': 'something else', 'name': 'something extra', 'borough': 'something better'}
        areaForm = AreaForm(form_data)
        self.assertFalse(areaForm.is_valid())
       
        self.assertFormError(areaForm, 'country', 'This field is required.')
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 1)

    # test AreaForm form city missing
    def test_AreaForm_city_missing(self):
        form_data = {'country': 'something else', 'name': 'something extra', 'borough': 'something better'}
        areaForm = AreaForm(form_data)
        self.assertFalse(areaForm.is_valid())
       
        self.assertFormError(areaForm, 'city', 'This field is required.')
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 1)

    # test AreaForm form borough missing
    def test_AreaForm_borough_missing(self):
        form_data = {'city': 'something else', 'name': 'something extra', 'country': 'something better'}
        areaForm = AreaForm(form_data)
        self.assertFalse(areaForm.is_valid())
       
        self.assertFormError(areaForm, 'borough', 'This field is required.')
        # assert how many errors there are 
        self.assertEqual(len(areaForm.errors), 1)


######################### TEST RATING FORM ###############################
    
    # test RatingForm form ideal input
    def test_RatingForm_ideal_input(self):
        form_data = {'description': 'something else', 'id': 2 }
        ratingForm = RatingForm(form_data)
        self.assertTrue(ratingForm.is_valid())
        # assert how many errors there are 
        self.assertEqual(len(ratingForm.errors), 0)

    # test RatingForm form description missing  == > there's no need to test id missing, becuase id is automatically given
    def test_RatingForm_description_missing(self):
        form_data = {'id': 2 }
        ratingForm = RatingForm(form_data)
        self.assertFalse(ratingForm.is_valid())
        # assert how many errors there are 
        self.assertEqual(len(ratingForm.errors), 1)
        self.assertFormError(ratingForm, 'description', 'This field is required.')

######################### TEST AREA RATING FORM ###############################
    
    # test AreaRatingForm form items missing becuase their fields allow null and blank values. 
    def test_Area_Rating_Form_missing_input(self):
        area_rating_form_data = {'homeless_sighting': 1, 'id': 2 }
        area_ratingForm = AreaRatingForm(area_rating_form_data)
        self.assertTrue(area_ratingForm.is_valid())
        # assert how many errors there are 
        self.assertEqual(len(area_ratingForm.errors), 0)
