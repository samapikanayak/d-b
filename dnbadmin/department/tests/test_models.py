from ..models import Department
from store.tests.test_models import BusinessUnitGroupModelTest

class DepartmentModelTest(BusinessUnitGroupModelTest):
    def create_department(self):
        business_code = BusinessUnitGroupModelTest.create_business_unit_grp(self)
        return Department.objects.create(name = "Name", business_unit_group_code=business_code, description="Description")
    def test_department(self):
        w = self.create_department()
        self.assertTrue(isinstance(w, Department))