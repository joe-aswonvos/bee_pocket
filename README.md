# Bee Pocket

The repository for my Code Institute Bootcamp capstone project.

## Table of Contents

1.  [Project Overview](#project-overview)
2.  [Technologies Used](#technologies-used)
3.  [Project Aims](#project-aims)
4.  [Application Breakdown](#application-breakdown)
    *   [admin\_app](#admin_app)
    *   [landing](#landing)
    *   [create\_app](#create_app)
    *   [pocket\_app](#pocket_app)
5.  [Features](#features)
6.  [Future Enhancements](#future-enhancements)
7.  [Credits](#credits)

## Project Overview

Bee Pocket is a web application designed to help families manage pocket money, tasks, behaviors, and rewards. It provides a centralized platform for parents or guardians to create and track tasks, assign consequences or rewards, and manage virtual "BeePockets" for their children.

## Technologies Used

*   **Python**: The primary programming language.
*   **Django**: A high-level Python web framework used for building the application.
*   **HTML**: Used for structuring the web pages.
*   **CSS**: Used for styling the web pages.
*   **JavaScript**: Used for adding interactivity to the web pages.
*   **Bootstrap**: A CSS framework used for creating responsive and mobile-first web pages.
*   **django-allauth**: A Django library used for handling user authentication, registration, and social authentication.
*   **psycopg2**: A PostgreSQL adapter for Python.
*   **Whitenoise**: A library for serving static files in Django.
*   **gunicorn**: A WSGI server for deploying the Django application.
*   **python-decouple**: Used to manage settings in Django projects.
*   **crispy-bootstrap5**: Used to render Django forms with Bootstrap styling.
*   **Material Icons**: Used to add icons to the web pages.

## Project Aims

The primary aims of this project are to:

*   Provide a user-friendly interface for managing pocket money and related activities.
*   Enable parents/guardians to easily create and assign tasks, consequences, and rewards.
*   Offer a virtual "BeePocket" system for tracking balances and transactions.
*   Implement user authentication and authorization for secure access.
*   Create a responsive and accessible web application.

## Application Breakdown

The project is structured into several Django apps, each serving a specific purpose:

### admin\_app

*   **Purpose**: Manages user accounts, BeePockets, and user permissions. Superusers can create and manage accounts, assign permissions to users for accessing specific BeePockets.
*   **Models**:
    *   `User`: Custom user model extending Django's AbstractBaseUser.
    *   `Account`: Represents a family account managed by a superuser.
    *   `BeePocket`: Represents a virtual pocket money account.
    *   `UserPermission`: Defines permissions for users to access BeePockets.

### landing

*   **Purpose**: Handles the landing page for the application. Displays marketing content to unauthenticated users and redirects authenticated users to their appropriate dashboard.
*   **Views**:
    *   `landing_page`: Renders the landing page based on user authentication status.

### create\_app

*   **Purpose**: Manages the creation, editing, and deletion of items (tasks, consequences, rewards) and item instances (specific transactions).
*   **Models**:
    *   `Item`: Represents a template for a transaction (e.g., "Clean your room").
     *   `Category`: Represents a category for an item (e.g. "Chores").
*   **Views**:
    *   `create_item`: Creates new items.
    *   `create_item_instance`: Creates new item instances.
    *   `item_instances`: Returns item instances for a given BeePocket.
    *   `approve_item_instance`: Approves an item instance.
    *   `edit_item`: Edits an existing item.
    *   `delete_item`: Deletes an existing item.
    *   `edit_item_instance`: Edits an existing item instance.
    *   `delete_item_instance`: Deletes an existing item instance.

### pocket\_app

*   **Purpose**: Provides the user dashboard for managing BeePockets and viewing item instances.
*   **Models**:
    *   `ItemInstance`: Represents a specific transaction in a BeePocket.
     *   `Comment`: Represents a comment on an item instance.
*   **Views**:
    *   `userpage`: Renders the user dashboard, displaying BeePockets, item instances, and balances.
    *   `item_detail`: Displays details for a specific item instance and allows users to add comments.

## Features

*   User authentication and registration using django-allauth.
*   Social authentication with Google and GitHub.
*   Account management by superusers.
*   Creation and management of BeePockets.
*   Assignment of user permissions for BeePocket access.
*   Creation and management of items (tasks, consequences, rewards).
*   Creation and management of item instances (transactions).
*   User dashboard for viewing BeePockets, balances, and item instances.
*   Commenting on item instances.
*   Responsive design for mobile and desktop devices.

## Future Enhancements

*   Implement automatic generation of item instances based on repeatability settings.
*   Add support for recurring transactions.
*   Implement a notification system for new tasks, consequences, and rewards.
*   Enhance the user interface with more interactive elements.
*   Add more detailed reporting and analytics.
*   Implement a mobile app version.

## Credits

*   [Code Institute](https://codeinstitute.net) - For providing the educational foundation and resources for this project.
*   [django-allauth](https://django-allauth.readthedocs.io/en/latest/) - For simplifying user authentication and social authentication.
*   [Bootstrap](https://getbootstrap.com) - For providing a responsive and mobile-first CSS framework.
*   All other libraries and technologies mentioned above.