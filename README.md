
Task Description: Build a Meal Ordering, Table Reservations, and Billing System Using Django
Comment
Objective:
In this task, you will build a Django web application that allows a restaurant to manage online meal orders, table reservations, and customer billing. The application will use Django's Model-View-Template (MVT) pattern, along with Django’s built-in authentication system, groups, and permissions.

Requirements:

1. User Roles (Using Django Groups and Permissions):
Admin:
Manage all resources (users, meals, orders, reservations, and bills).
View all reservations, orders, and associated billing details.
Customer:
Can browse meals, make table reservations, place meal orders, and view their bills.
Can only view their own reservations, orders, and bills.
Authentication System:

Use Django’s built-in user authentication system for sign-up, login, logout, and session management.
Leverage Django groups and permissions to manage role-based access (Admin and Customer):
Users who sign up are automatically added to the Customer group.
Admin users are created via the Django admin panel and added to the Admin group.
Implement role-based access control:
Admins should have access to the admin dashboard and management features.
Customers should have access to order meals, make reservations, and view bills.
Note: 
Make sure that Customers can only see their own orders and bills, not all orders or bills in the system.

2. Features:
2.1. User Authentication:
Implement user registration (for customers only), login, and logout using Django’s built-in authentication system.
Use Django groups to assign the appropriate roles:
Users who sign up are automatically added to the Customer group.
Admin users are created via the Django admin panel and added to the Admin group.
Implement role-based access control:
Admins should have access to the admin dashboard and management features.
Customers should only have access to order meals, make reservations, and view their own bills and order history.
2.2. Meal Management:
Admin users can add, edit, and delete meals.
Each meal must include: name, description, price, and availability (in stock/out of stock).
Customers can browse the menu and select meals for their orders.
2.3. Table Reservations:
Customers can reserve tables by selecting a date, time, and the number of guests.
Ensure table availability is tracked, preventing double-booking for the same time slot.
Reservations should be linked to the logged-in customer.
2.4. Meal Ordering:
Customers can place meal orders by selecting one or more meals.
Each order should include the meal details, quantity, total price, and order status (pending, completed).
Customers should be able to view their order history and track the status of their orders.
2.5. Billing:
After an order is placed, the system should automatically generate a bill.
Bill Details should include:
Linked customer and order details.
Total price of the order.
Payment status (unpaid, paid).
Customers can view their bills and mark them as paid (simulated, without real payment integration).
Admin can manage bills, including changing the payment status.
2.6. Admin Dashboard:
Admin users should have access to a dashboard where they can:
Manage users, meals, orders, reservations, and bills.
Track the statuses of reservations, orders, and payments.
3. Database Structure:
User: Django’s built-in User model with groups (Admin, Customer).
Meal: name, description, price, availability.
Order: customer (linked to User), list of meals, total price, order status (pending, completed).
Reservation: customer (linked to User), table number, date, time.
Bill: order (linked to Order), total price, payment status (unpaid, paid).
4. Project Guidelines:
Use Django’s MVT architecture and the Django ORM to interact with the database.
Implement CRUD operations for meals, orders, reservations, and bills.
Use Django forms for user input on meal ordering, table reservations, and bill payments.
Render views using Django templates with server-side rendering.
Ensure role-based navigation between pages:
Admins should see a dashboard with links to manage meals, reservations, orders, and bills.
Customers should see the meal menu, reservation form, order history, and billing information.
5. Bonus (Optional):
Add meal search and filtering functionality (e.g., by price, availability).
Implement Menu model with implementing CRUD with templates.
Implement email notifications for order and reservation confirmations.
Add pagination on the meal and order history pages.
Submission Requirements:
Submit the project via GitHub with a well-organized folder structure and depending on the flow that we have agreed on.
Include a README.md file that explains how to set up and run the project, detailing installation steps, dependencies, and any setup required.
Ensure your project follows Django’s best practices, including proper use of models, views, templates, forms, and groups/permissions.
Your project must be connected to a MySQL database with proper setup instructions included in the README.

