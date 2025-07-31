# =======================================================================
# FILE: myduka/users/tests.py (NEW)
# =======================================================================
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserAPITests(TestCase):
    """
    Test suite for the users app API endpoints.
    """

    def setUp(self):
        """
        Set up the necessary objects for the tests.
        """
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        """
        Ensures that a user was created correctly in the setup.
        """
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'testuser')

    def test_merchant_registration_api(self):
        """
        Tests the merchant registration API endpoint.
        """
        new_merchant_data = {
            'username': 'newmerchant',
            'email': 'merchant@example.com',
            'password': 'password123'
        }
        response = self.client.post('/api/v1/auth/register/', new_merchant_data, format='json')
        
        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that a new user was created with the correct role
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(username='newmerchant')
        self.assertEqual(new_user.role, User.Role.MERCHANT)

    def test_user_login_api(self):
        """
        Tests the user login API endpoint and token generation.
        """
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/v1/auth/login/', login_data, format='json')

        # Check that the login was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that access and refresh tokens are present in the response
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

# =======================================================================
# FILE: myduka/stores/tests.py (NEW)
# =======================================================================
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from .models import Store, InventoryItem, SupplyRequest

class StoreAPITests(TestCase):
    """
    Test suite for the stores app API endpoints.
    """

    def setUp(self):
        """
        Set up the necessary objects for the tests.
        This method is run before each test.
        """
        # Create a merchant user who will own the store
        self.merchant = User.objects.create_user(username='testmerchant', password='password123', role=User.Role.MERCHANT)
        
        # Create a store owned by the merchant
        self.store = Store.objects.create(name='Test Duka', location='Nairobi', owner=self.merchant)
        
        # Create an admin and a clerk for the store
        self.admin = User.objects.create_user(username='testadmin', password='password123', role=User.Role.ADMIN, store=self.store)
        self.clerk = User.objects.create_user(username='testclerk', password='password123', role=User.Role.CLERK, store=self.store)

        # Create an inventory item for testing
        self.inventory_item = InventoryItem.objects.create(
            store=self.store,
            name='Sugar',
            quantity=100,
            buying_price=100,
            selling_price=120
        )

        # Initialize the API client
        self.client = APIClient()

    def test_inventory_item_creation(self):
        """
        Ensures that an inventory item was created correctly in the setup.
        """
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(self.inventory_item.name, 'Sugar')
        self.assertEqual(self.inventory_item.store, self.store)

    def test_clerk_can_request_stock_successfully(self):
        """
        Tests the "happy path" for a clerk requesting stock that exists.
        """
        # Authenticate the client as the clerk
        self.client.force_authenticate(user=self.clerk)

        # The data the clerk's frontend would send
        request_data = {
            'product_name': 'Sugar',
            'quantity_requested': 10
        }

        # Make a POST request to the supply requests endpoint
        response = self.client.post('/api/v1/supply-requests/', request_data, format='json')

        # Assert that the request was successful (201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Assert that a new supply request was created in the database
        self.assertEqual(SupplyRequest.objects.count(), 1)
        self.assertEqual(SupplyRequest.objects.first().quantity_requested, 10)

    def test_clerk_request_for_nonexistent_stock_fails(self):
        """
        Tests the "unhappy path" where a clerk requests a product that is not in the inventory.
        """
        # Authenticate the client as the clerk
        self.client.force_authenticate(user=self.clerk)

        # The data for a product that does not exist
        request_data = {
            'product_name': 'Salt',
            'quantity_requested': 5
        }

        # Make a POST request
        response = self.client.post('/api/v1/supply-requests/', request_data, format='json')

        # Assert that the request failed with a 400 Bad Request error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert that no new supply request was created
        self.assertEqual(SupplyRequest.objects.count(), 0)
        # Assert that the correct error message was returned
        self.assertIn("not found in your store's inventory", str(response.data))
