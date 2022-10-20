from django.test import TestCase

from accounts.models import Account
from company.models import Company
from django.utils import timezone

from contractors.models import Contractor
from customuser.models import CustomUser, User_Account


# models test
from transactions.models import Transaction


class CompanyModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(email='test@gmail.com', password='Kirill22',
                                         date_joined=timezone.now())
        User_Account.objects.create(owner=user, name=user.email)

    def get_user_account(self):
        return User_Account.objects.last()

    def create_company(self, company_name="MaskPlanet"):

        company, status = Company.objects.get_or_create(company_name=company_name, date_joined=timezone.now(),
                                      uid='334e3af3-648f-455d-b100-effbc2060268', user_account=self.get_user_account())
        return company

    def create_contractor(self, contractor_name='Kiryl Kazlavets'):
        contractor, status = Contractor.objects.get_or_create(user_account=self.get_user_account(), contractor_name=contractor_name,
                                         uid='334e3af3-648f-455d-b100-effbc2061258')
        return contractor

    def create_account(self, account_id='PL64359015740000380146865941'):
        account, status = Account.objects.get_or_create(user_account=self.get_user_account(), uid='464e27f3-648f-455d-b100-effbc2079538',
                                      account_id=account_id, company=self.create_company(), bank='Santander Bank',
                                      currency='USD', date_joined=timezone.now())
        return account

    def create_transaction(self):
        transaction, status = Transaction.objects.create(uid='664e27f3-648f-455d-b100-effbc2079126', user_account=self.get_user_account(),
                                                         transaction_type='Income', sum_of_transactions=36, transaction_id='Y35HREF',
                                                         company=self.create_company(), account=self.create_account(),
                                                         contractor=self.create_contractor())
        return transaction

    def test_company_create(self):
        w = self.create_company()
        self.assertTrue(isinstance(w, Company))
        self.assertEqual(w.__str__(), w.company_name)

    def test_contractor_create(self):
        w = self.create_contractor()
        self.assertTrue(isinstance(w, Contractor))
        self.assertEqual(w.__str__(), w.contractor_name)

    def test_account_create(self):
        w = self.create_account()
        self.assertTrue(isinstance(w, Account))
