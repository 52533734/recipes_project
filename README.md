# Recipes Web Application

## Overview
This is a Django-based web application that allows users to browse, search, and view recipes from an open dataset. Registered users can log in and add recipes to their wishlist for future reference.

The application is database-driven and includes a fully functional front-end with list and detail pages, search and filter capabilities, and basic user interaction.

## Features
- Browse a list of recipes with name, cuisine, and published date.
- View detailed recipe pages including ingredients and instructions.
- Search recipes by name or ingredient.
- Filter recipes by cuisine type.
- User registration and login.
- Wishlist feature for logged-in users.
- Basic validation and error handling.
- Automated test coverage for core functionality and edge cases.

## Dataset
- Source: Custom dataset (subset of 40+ recipes)
- Format: CSV (`data/recipes.csv`)
- Sample fields: `name`, `ingredients`, `cuisine`, `description`, `instructions`

## Technology Stack
- Python 3.13.7
- Django 6.0.3
- SQLite database (default)
- HTML/CSS for templates

## Setup Instructions

1. **Clone the Repository**
Bash
    git clone <repository-url>
    cd recipes_project

2. **Create and Activate a Virtual Environment**
Bash
    python -m venv venv
    venv\Scripts\activate   # for Windows
    or 
    source venv/bin/activate  # for macOS/Linux

3. **Install Dependencies**
Bash
    pip install -r requirements.txt

4. **Apply Migrations**
Bash
    python manage.py migrate

5. **Import Recipes from CSV**
Bash
    python manage.py import_recipes

6. **Run the Development Server**
- Bash
    python manage.py runserver
- Open http://127.0.0.1:8000 in your browser.

## Running Tests
- Bash
    python manage.py test recipes
- Includes 15 automated tests covering registration, login, recipe list/detail, search/filter, wishlist, and edge cases.

## Notes
- All pages include basic validation and error handling.
