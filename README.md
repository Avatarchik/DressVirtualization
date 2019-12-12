# Perfect-Fit - Dress Virtualization
This is a project for CS 4800 - Software Engineering. For this project, we created a virtual dressing room for bridal dresses. The application uses Django Web Framework along with THREE.js. We used a 3D model and overlay transparent PNG images on top of the model to give an illusion of the model wearing the dress. 


## Getting Started
For the best results, please use a Linux System. The project was created on a Linux environment and has not been tested on other OS. 
If you don't have Linux OS then download VMware or VirtualBox and install a Linux distro. 


### Prerequisites
- Python 3.7.5
- OpenCV 4.1.2
- Django 3.0 
- Pillow 
- Django storages 
- Django crispy Forms 
"Required packages will be install when run 'pip install -r requirements.txt'"


### Installing
1) (Optional but recommended) Use Linux OS
2) Install a virtual environment
3) Download the project source code to your virtual environment. 
4) Run "pip install -r requirements.txt" to install necessary project packages. 
5) cd to "FittingRoom/Project" (same directory as manage.py and makefile)
6) Run "make" or "python3 manage.py runserver" to run the server
7) Type localhost:8000 in your preferred browswer


## Deployment

1) Create Heroku Account
2) Run "heroku create application-name"
3) Create Procfile
4) Change "STATIC_ROOT" to "staticfiles"
5) Run "git push heroku master"


## Built With
* [Django](https://docs.djangoproject.com/en/3.0/) - The web framework used
* [OpenCV](https://docs.opencv.org/4.1.2/) - Used with image modifications
* [THREE.js](https://threejs.org/docs/) - Used for graphics and animations of the 3D model


## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
