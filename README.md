# MustafaAlperenCihan-HW2
# Flask User Authentication and Profile Management System

This Flask application demonstrates a simple user authentication system with extended functionalities for user profile management. Users can register, log in, update their profile information, change their passwords, and upload a profile picture.

## Features

- **User Registration**: Allows new users to create an account by providing a username and password. Each user's password is hashed with sha-256 for security before being stored in the database.

- **User Login**: Authenticates users by their username and password. Upon successful authentication, users are redirected to their profile page.

- **Logout**: Users can log out of the application, which clears their session data.

- **Profile Page**: Authenticated users can view their profile page, which displays their username, name, email, and profile picture.

- **Default Profile Picture**: New users are assigned a default profile picture upon registration. Users can update their profile picture at any time.

- **Update Profile**: Users can update their profile information, including their name, email, and profile picture.

- **Change Password**: Users have the option to change their password from their profile page.

## Technology Stack

- **Frontend**: HTML, CSS
- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Password Hashing**: SHA-256
