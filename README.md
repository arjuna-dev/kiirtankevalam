# Kiirtan Kevalam

### Kiirtan Kevalam is a web app to let users share music, namely Kiirtan, Bhajan and Prabhat Samgiita songs alongside with the western chords to play them.

#### _It was created with the yoga and meditation group Ananda Marga in mind._

___


## Installation Instructions

* Install Python 3 
* Install virtualenv in the terminal: 

  `$ pip install virtualenv`
* Create a new virtual environment in the terminal:

  `$ virtualenv ENV`  _(where ENV is a directory to place the new virtual environment)_
* Clone this repository into your virtual environment folder (ENV)
* Activate your virtual environment like this:

  * From the terminal open the folder where you created your virtual environment (ENV). 
  * In the terminal do `$ ls`
  * A folder called "bin" should be listed
  * In the terminal do `$ source bin/activate`
* Open the repository folder, open ebdjango folder (`ebdjango/ebdjango` file path) and install de requirenments from the text file "requirenments.txt" like this:

  * `$ cd ebdjango`
  * `$ cd ebdjango`
  * `$ pip install -r requirenments.txt`

That's it! 😁

___


## Run the web app on a local server

* From the terminal place yourself on `ebdjango/ebdjango` file path.

  _(Doing `$ ls` command on the terminal should list the file called "manage.py")_
* On the terminal do `$ python manage.py runserver`

___

## About

Kiirtan Kevalam is a django web application. For the front end it uses JQuery and Bootstrap4 libraries.

It is currently deployed for testing on the domain [kiirtan.org](http://kiirtan.org/ "For small kind beta testing")



















