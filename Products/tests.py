from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Products.models import Tables, Order

class ChangeOrderTableTestCase(TestCase):
    def setUp(self):
        # Create RestaurantDetails
        from Products.models import RestaurantDetails
        self.rest_details = RestaurantDetails.objects.create(
            Name_of_restaurant="Test Restaurant",
            TRN="12345",
            location="Test Location",
            print_copies=2
        )
        
        # Create users
        self.user = User.objects.create_user(username='testwaiter', password='testpassword')
        
        # Create tables
        self.table1 = Tables.objects.create(Table_number=1, Number_of_Seats=4)
        self.table2 = Tables.objects.create(Table_number=2, Number_of_Seats=2)
        
        # Create order
        self.order = Order.objects.create(table=self.table1, user=self.user)
        
        # Client
        self.client = Client()
        self.client.login(username='testwaiter', password='testpassword')

    def test_change_order_table_success(self):
        url = reverse('change_order_table', args=[self.order.id])
        # Submit POST request with table_id
        response = self.client.post(url, {'table_id': self.table2.id})
        
        # Verify redirect
        self.assertEqual(response.status_code, 302)
        
        # Refresh order from DB
        self.order.refresh_from_db()
        self.assertEqual(self.order.table, self.table2)

    def test_change_order_table_non_existent_table(self):
        url = reverse('change_order_table', args=[self.order.id])
        # Submit POST request with non-existent table_id
        response = self.client.post(url, {'table_id': 9999})
        
        # Should return 404
        self.assertEqual(response.status_code, 404)

    def test_change_order_table_get_redirect(self):
        url = reverse('change_order_table', args=[self.order.id])
        # GET request should just redirect
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
        # Verify table has not changed
        self.order.refresh_from_db()
        self.assertEqual(self.order.table, self.table1)

    def test_receipt_copy_num(self):
        url = reverse('receipt', args=[self.order.id])
        # Verify normal receipt load
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "- CUSTOMER COPY -")
        
        # Verify copy=1 load (Customer copy only)
        response = self.client.get(url, {'copy': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "- CUSTOMER COPY -")
        
        # Verify copy=2 load (Store copy only)
        response = self.client.get(url, {'copy': '2'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "- STORE COPY -")


class AddOnsTestCase(TestCase):
    def setUp(self):
        # Create RestaurantDetails
        from Products.models import RestaurantDetails, FoodCategory, Menu, AddOns, Order, OrderItem
        self.rest_details = RestaurantDetails.objects.create(
            Name_of_restaurant="Test Restaurant",
            TRN="12345",
            location="Test Location",
            print_copies=2
        )
        
        # Create users
        self.user = User.objects.create_user(username='testwaiter', password='testpassword')
        
        # Create tables
        self.table = Tables.objects.create(Table_number=1, Number_of_Seats=4)
        
        # Create Category & Menu
        self.category = FoodCategory.objects.create(name="Beverage")
        self.menu_item = Menu.objects.create(category=self.category, name="Latte", price=15.0, status=True, stock=100, tax="Inclusive", potion="Medium", diet="Veg")
        
        # Create AddOns
        self.addon_extra_shot = AddOns.objects.create(name="Extra Shot", price=3.0, status=True)
        self.addon_syrup = AddOns.objects.create(name="Vanilla Syrup", price=2.0, status=True)
        
        # Create order & OrderItem
        self.order = Order.objects.create(table=self.table, user=self.user)
        self.order_item = OrderItem.objects.create(order=self.order, menu_item=self.menu_item, quantity=2, price=15.0)
        
        # Client
        self.client = Client()
        self.client.login(username='testwaiter', password='testpassword')

    def test_addons_price_calculation(self):
        # Initial price total without addons
        self.assertEqual(self.order_item.get_total_price(), 30.0)
        
        # Add addons
        self.order_item.add_ons.add(self.addon_extra_shot, self.addon_syrup)
        
        # get_total_price should now sum addons and multiply by quantity
        # 2 * (15.0 + 3.0 + 2.0) = 40.0
        self.assertEqual(self.order_item.get_total_price(), 40.0)

    def test_add_on_to_item_view(self):
        url = reverse('add_on_to_item', args=[self.order_item.id, self.order.id])
        data = {
            'instraction': 'Less sweet',
            'addons': [self.addon_extra_shot.id, self.addon_syrup.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirects back to OrderSingle
        
        # Refresh from database and check
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.special_instructions, 'Less sweet')
        self.assertEqual(list(self.order_item.add_ons.all()), [self.addon_extra_shot, self.addon_syrup])

    def test_ajax_increase_quantity_has_addons_context(self):
        # Call increase_quantity AJAX
        url = reverse('increase_quantity')
        response = self.client.post(url, {'item_id': self.order_item.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        # Check response content contains the updated values and addon list
        data = response.json()
        self.assertIn('order_html', data)
        self.assertIn('Latte', data['order_html'])
        self.assertIn('Extra Shot', data['order_html'])

    def test_ajax_decrease_quantity_has_addons_context(self):
        # Call decrease_quantity AJAX
        url = reverse('decrease_quantity')
        response = self.client.post(url, {'item_id': self.order_item.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn('order_html', data)
        self.assertIn('Latte', data['order_html'])

    def test_delete_menuitem_view(self):
        url = reverse('Delete_menuitem', args=[self.order_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirects back to OrderSingle
        
        # Verify it is deleted from the database
        from Products.models import OrderItem
        self.assertFalse(OrderItem.objects.filter(id=self.order_item.id).exists())
