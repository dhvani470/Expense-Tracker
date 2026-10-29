# Expense Tracker

A web-based Expense Tracker built with Django and Python to help users manage daily expenses, monitor monthly budgets, visualize spending patterns, and analyze their financial activities.

## Overview

Expense Tracker is a web application that allows users to record and organize their expenses through a simple, user-friendly interface. It provides a dashboard for tracking spending, budgeting tools, interactive charts, and expense analysis to help users understand their spending habits.

## Features

- **User Authentication:** Register and log in to your account.
- **Expense Management:** Add, edit, and delete expenses.
- **Dashboard:** View expense summaries and monthly spending.
- **Expense Filtering:** Filter records by category, payment method, date range, and search keywords.
- **Category Management:** Organize expenses by category.
- **Payment Methods:** Record payments made through Cash, UPI, Card, or Bank Transfer.
- **Monthly Budget:** Set a monthly budget and monitor spending and remaining balance.
- **Interactive Charts:** Visualize expense data using charts.
- **Expense Analysis:** View total spending, average expenses, category summaries, and monthly summaries.
- **jQuery Validation:** Validate expense forms before submission.
- **Delete Confirmation:** Confirm before deleting an expense.
- **Notifications:** Display messages for application actions.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| Bootstrap 5 | User interface and responsive design |
| JavaScript | Client-side functionality |
| jQuery | Form validation and interactive behavior |
| Chart.js | Data visualization |
| Pandas | Expense data analysis |

## Project Structure

```text
Expense-Tracker/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── expenses/
│   ├── migrations/
│   ├── static/
│   │   └── expenses/
│   │       ├── app.js
│   │       └── style.css
│   ├── templates/
│   │   └── expenses/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── dashboard.html
│   │       ├── add_expense.html
│   │       ├── budget.html
│   │       ├── charts.html
│   │       └── analysis.html
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
├── manage.py
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: The structure above represents the main application files. Your local project may contain additional files.*

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/dhvani470/Expense-Tracker.git
cd Expense-Tracker
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

**macOS and Linux:**

```bash
source venv/bin/activate
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

If a `requirements.txt` file is available, run:

```bash
pip install -r requirements.txt
```

Otherwise, install the required packages:

```bash
pip install django pandas
```

### 5. Apply Database Migrations

```bash
python manage.py migrate
```

### 6. Create an Administrator Account

To access the Django administration panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to enter your username, email address, and password.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Open the following addresses in your browser:

- **Application:** http://127.0.0.1:8000/
- **Django Admin:** http://127.0.0.1:8000/admin/

## How to Use

1. Open the application in your browser.
2. Register a new account.
3. Log in using your credentials.
4. Add expenses by entering the amount, category, date, description, and payment method.
5. View your expenses on the dashboard.
6. Use filters to find specific expense records.
7. Set a monthly budget and monitor your spending.
8. Visit the Charts page to visualize spending patterns.
9. Visit the Analysis page to review expense summaries and monthly trends.
10. Edit or delete expenses when necessary.

## Database

The application uses SQLite, Django's default database.

The main database models include:

- **Category:** Organizes expenses into categories.
- **Expense:** Stores expense details, including amount, category, date, description, payment method, and associated user.
- **Budget:** Stores monthly budget information for individual users.

Database migrations are managed using Django's migration system.

## Security

- User authentication is handled by Django.
- Expense records are associated with their respective users.
- Passwords are managed by Django's authentication system.
- Local database files and environment files should not be committed to a public repository.
- For production deployment, configure secure settings, environment variables, and an appropriate database.

## Project Objectives

- Develop a practical web application using Django.
- Implement user authentication and database operations.
- Apply CRUD operations to manage expense records.
- Create a responsive interface using Bootstrap and CSS.
- Use jQuery for client-side form validation and interactive behavior.
- Present spending information through charts and data analysis.
- Understand the integration of frontend and backend technologies.

## Future Enhancements

- Export expense reports to CSV or PDF.
- Add recurring expenses.
- Introduce spending limits and budget alerts.
- Add detailed reports and date-based comparisons.
- Support additional chart types and financial summaries.

## License

This project was developed for educational purposes as part of an Open Source Technologies course.

## Author

**Dhvani Mangukiya**
