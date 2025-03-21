# JSV

## Overview
<!--
JSV is an enterprise system aimed at implementing requisition, purchasing, and inventory management for the enterprise. This guide will help you set up the project on your local machine for development and testing purposes.
-->
This guide will help you set up the project on your local machine for development and testing purposes.

## Prerequisites
- Python 3.x
- Git

## Getting Started

### Cloning the Repository
To clone the repository, run the following command in your terminal:
```sh
git clone https://github.com/lanlines/jsv.git
cd jsv
```

### Creating a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. You can create a virtual environment using `venv`:
```sh
python -m venv venv
```

Activate the virtual environment:
- On Windows:
  ```sh
  .\venv\Scripts\activate
  ```


### Installing Requirements
Once the virtual environment is activated, install the required packages using `pip`:
```sh
pip install -r requirements.txt
```
Install Pillow (if not already installed):
```sh
python -m pip install Pillow
```
Run migrations:
```sh
python manage.py makemigrations
python manage.py migrate
```

Run the development server:
```sh
python manage.py runserver
```

## Usage
[Instructions on how to use the project]

## Contributing
[Instructions on how to contribute to the project]

## License
[License information]

## Contact
For any questions or issues, please contact [Your Contact Information].
