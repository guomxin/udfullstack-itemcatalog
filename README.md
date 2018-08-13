# Introduction
This project is a RESTful web application utilizing the Flask framework which accesses a database that populates categories and their items. OAuth2 provides authentication for CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

# Dependencies
- [Vagrant](https://www.vagrantup.com/)
- [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

# Installation
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`)
4. Log into Vagrant VM (`vagrant ssh`)
5. Navigate to the code directory
6. Setup application database `python database_setup.py`
7. Insert fake data `python create_data.py`
8. Run application using `python application.py`
9. Access the application locally using http://localhost:8080

# Google Login
To get Google login working there are a few additional steps:
1. Go to [Google Dev Console](https://console.developers.google.com) and login
2. Go to Credentials
3. Select Create Crendentials > OAuth Client ID
4. Select Web application
5. Authorized JavaScript origins = 'http://localhost:8080'
6. Select Create
7. Copy the Client ID and paste it into the `data-clientid` in login.html
8. On the Dev Console Select Download JSON
9. Rename JSON file to client_secrets.json

# JSON Endpoints
Categories JSON: `/api/catalog/JSON`
- Get all categories
Category Items JSON: `/api/catalog/<int:category_id>/items/JSON/`
- Get all items for a specific category
Item JSON: `/api/catalog/item/<int:item_id>/JSON/`
- Get a specific item
