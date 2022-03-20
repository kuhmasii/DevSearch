from django.contrib.auth import get_user_model
from userapp.models import Profile
from django.test import TestCase
from .models import Project, Tag, Review


User = get_user_model()

class ProjectTests(TestCase):

    def setUp(self):
        User.objects.create(username='kuhmasii')
        Tag.objects.create(name='django')
        prof = Profile.objects.get(user__username='kuhmasii')
        proj = Project.objects.create(title='Testing Database', owner=prof)
        Project.objects.create(title='No review', owner=prof)
        Review.objects.create(project=proj, owner=prof, body='This is a review test')

    def test_project_creation(self):

        """Testing an instance of a Project model created.
        Instance should return the data of a title attribute as 
        the '__str__' of the model, class Project.
        """
        obj = Project.objects.get(title__iexact='Testing Database')
        expected_obj_title = str(obj.title)

        self.assertTrue(isinstance(obj, Project)) 
        self.assertEqual(obj.__str__(), expected_obj_title)

    def test_not_project_creation(self):

        """Testing an instance of a Project model is not created.
        """
        obj = Project.objects.get(title__iexact='Testing Database')
        not_obj = 'This is just a dummy word'
        self.assertFalse(isinstance(not_obj, Project))
        self.assertNotEqual(obj.__str__(), not_obj)

    def test_data_for_instance_of_project_model(self):
        """
        Testing an instance data is correct
        """
        ins = Project.objects.get(title__iexact='Testing Database')
        self.assertEqual(ins.title, 'Testing Database')

    def test_data_not_for_instance_of_project_model(self):
        """
        Testing an instance data is not correct
        """
        ins = Project.objects.get(title__iexact='Testing Database')
        self.assertNotEqual(ins.title, 'This is not your data')

    def test_get_reviews_with_value(self):
        """
        get_reviews method should return all reviews query
        with the uuid.
        """
        ins = Project.objects.get(title__iexact='Testing Database')
        owner_id = ins.owner_id.hex
        reviews = [x.hex for x in ins.get_reviews()]
        self.assertIn(owner_id, reviews)

    def test_get_reviews_without_value(self):
        """
        get_reviews method should return empty query
        """
        ins = Project.objects.get(title__iexact='No review')
        self.assertFalse(ins.get_reviews())

    def test_get_tag_with_value(self):
        """
            get_tag method should return all tags query.
        """
        ins = Project.objects.get(title__iexact='Testing Database')
        get_tag = Tag.objects.get(name__iexact='django')
        ins.tag.add(get_tag)
        check = [x.name for x in ins.get_tag()]

        self.assertTrue(check)
        self.assertIn('django', check)

    def test_get_tag_without_value(self):
        """
        get_tag method should return an empty query.
        """
        ins = Project.objects.get(title__iexact='Testing Database')
        check = [x.name for x in ins.get_tag()]
        self.assertFalse(check)

    def test_featuredImageUrl_with_value(self):
        """
            project_image method should return a url path
        """

        ins = Project.objects.get(title__iexact='Testing Database')
        url = ins.featuredImageUrl
        self.assertEqual(url, '/media/mypics/default.jpg')

	# def test_featuredImageUrl_without_value(self):
	# 	"""
	# 	project_image method should return an empty string
	# 	"""
	# 	ins = Project.objects.get(title__iexact='Testing Database')
	# 	url = ins.featuredImageUrl
	# 	print(url)
	# 	self.assertFalse(url)

class TagTests(TestCase):

	def setUp(self):
		Tag.objects.create(name='django')

	def test_tag_creation(self):

		"""Testing an instance of a Tag model created.
			Instance should return the data of a name attribute as 
			the '__str__' of the model, class Tag.
		"""
		obj = Tag.objects.get(name__iexact='django')
		expected_obj_name = str(obj.name)

		self.assertTrue(isinstance(obj, Tag))
		self.assertIsInstance(obj,Tag) 
		self.assertEqual(obj.__str__(), expected_obj_name)
	
	def test_not_tag_creation(self):
		
		"""Testing an instance of a Tag model is not created.
		"""
		obj = Tag.objects.get(name__iexact='django')
		not_obj = 'This is just a dummy word'
		
		self.assertFalse(isinstance(not_obj, Tag))
		self.assertNotIsInstance(not_obj,Tag) 
		self.assertNotEqual(obj.__str__(), not_obj)

	def test_data_for_instance_of_tag_model(self):
		"""
		Testing an instance data is correct
		"""
		ins = Tag.objects.get(name__iexact='django')
		self.assertEqual(ins.name, 'django')


	def test_data_not_for_instance_of_tag_model(self):
		"""
		Testing an instance data is not correct
		"""
		ins = Tag.objects.get(name__iexact='django')
		self.assertNotEqual(ins.name, 'This is not your data')


class ReviewTests(TestCase):
    
    def setUp(self):
        proj = Project.objects.create(title='Testing Database')
        Review.objects.create(body='this is a test review', project=proj)

    def test_review_creation(self):

        """Testing an instance of a Review model created.
            Instance should return the data of a value attribute as 
            the '__str__' of the model, class Review.
        """
        obj = Review.objects.get(body__iexact='this is a test review')
        expected_obj_name = str(obj.value)

        self.assertTrue(isinstance(obj, Review))
        self.assertIsInstance(obj,Review) 
        self.assertEqual(obj.__str__(), expected_obj_name)

    def test_not_review_creation(self):

        """Testing an instance of a Review model is not created.
        """
        obj = Review.objects.get(body__iexact='this is a test review')
        not_obj = 'This is just a dummy word'

        self.assertFalse(isinstance(not_obj, Review))
        self.assertNotIsInstance(not_obj,Review) 
        self.assertNotEqual(obj.__str__(), not_obj)

    def test_data_for_instance_of_review_model(self):
        """
        Testing an instance data is correct
        """
        ins = Review.objects.get(body__iexact='this is a test review')
        self.assertEqual(ins.body, 'this is a test review')


    def test_data_not_for_instance_of_review_model(self):
        """
        Testing an instance data is not correct
        """
        ins = Review.objects.get(body__iexact='this is a test review')
        self.assertNotEqual(ins.body, 'This is not your data')
