from email import header
from django.test import TestCase, Client
from django.urls import reverse
from party.models import Language
from store.models import BusinessUnitGroup
from ..models import Department
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):
    def authenticate(self):
        self.login_url = reverse('signin')
        self.user_data = {
            'username': 'dnbadmin',
            'password': 'dnbsupply',
            'email': 'testdbsupply@dbsupply.com'
        }
        user = User.objects.create(username=self.user_data["username"], email = self.user_data["email"])
        user.set_password(self.user_data["password"])
        user.save()
        res = self.client.post(self.login_url, {'username': user.username, 'password': self.user_data["password"]})
        respone = res.json()
        print(respone)
        self.token = respone["access"]
        self.header = {
            "HTTP_AUTHORIZATION":f"Bearer {self.token}"
        }

class DepartmentListCreate(AuthenticationTest):
    def setUp(self) -> None:
        self.client = Client()
        self.language_data = Language.objects.create(ID_LGE= "some",NM_LGE= "some")
        self.businessunit = BusinessUnitGroup.objects.create(ID_LGE=self.language_data, NM_BSNGP="desc")
        self.department_data = {
            "name": "dept1",
            "business_unit_group_code": self.businessunit.ID_BSNGP,
            "description": "department description 1"
        }
    def test_create_department_wa_auth(self):
        self.url = reverse("department")
        self.authenticate()
        response = self.client.post(self.url,self.department_data)
        self.assertEqual(response.status_code, 401)
    def test_create_department_with_auth(self):
        self.url = reverse("department")
        self.authenticate()
        response = self.client.post(self.url,self.department_data, **self.header)
        self.assertEqual(response.status_code, 201)
    def test_department_list_wa_auth(self):
        self.url = reverse("department")
        self.authenticate()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
    def test_department_list_with_auth(self):
        self.url = reverse("department")
        self.authenticate()
        response = self.client.get(self.url, **self.header)
        self.assertEqual(response.status_code, 200)






