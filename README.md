# Business Intelligence System for a Veterinary Clinic

This BI System is created to assist the veterinarians employed in a veterinart clinic, in the decision-making process of what drugs / prescriptions should be avoided for the animals they are looking after.

In order to run it in your machine the following steps must be followed

## PostGreSQL Setup Steps

First of all you have to install PostGreSQL using postgres installer 

###### Step 1:

Download Postgres Installer [here](https://www.postgresql.org/download/)

###### Step 2:

Click on the executable file to run the installer.

###### Step 3:

Select your preferred language.


![PGInstaller-GUI-installer-13](https://user-images.githubusercontent.com/24418024/150790398-3b5b267f-ce0b-420d-a165-742d75d2a8d0.jpg)


###### Step 4:

Specify directory where you want to install PostgreSQL.


![PGInstaller-GUI-installer3](https://user-images.githubusercontent.com/24418024/150790429-060a5885-3881-49ee-a6bb-95ec33701c47.jpg)


###### Step 5:

Specify PostgreSQL server port. You can leave this as default if you’re unsure what to enter.


![PGInstaller-GUI-installer](https://user-images.githubusercontent.com/24418024/150790451-16398af2-6750-4fbc-a55c-bdb39ab7a52b.jpg)


###### Step 6:

Specify data directory to initialize PostgreSQL database.

![PGInstaller-GUI-installer5](https://user-images.githubusercontent.com/24418024/150790757-c437ef1b-1e98-4255-a7d3-8143bf88f9e0.jpg)


###### Step 7:

Create a PostgreSQL user password.

![PGInstaller-GUI-installer6](https://user-images.githubusercontent.com/24418024/150790812-4df0e3a0-d60d-4592-adab-a869b97622f7.jpg)



###### Step 8:

Create password for database Superuser.

![PGInstaller-GUI-installer7](https://user-images.githubusercontent.com/24418024/150790802-9d3507c9-3db7-487f-a98d-a05a3b9f0844.jpg)


###### Step 9:

Click next to begin PostgreSQL installation


###### Step 10:

Press Finish

![PGInstaller-GUI-installer11](https://user-images.githubusercontent.com/24418024/150818960-add32e85-aa7d-4b2b-8548-d140b437b4ca.jpg)

The readme file contains installation paths, service names and database credentials.

## IDE Setup / Project Import Steps

###### Step 1

Download the project and import it via your (ideally) Pycharm IDE, or clone it!


###### Step 2

Install the following libraries using pip, with the following commands:

```
pip install psycopg2
pip install pandas
pip numpy
```

###### Step 3

Enter your DB's credentials in the ```init.py``` file .
Unless you used banana_2 as a password you will want to change that, the rest are the default values.


###### Step 4

On the top right of your Pycharm IDE choose PostgreSQL as data source

![Screenshot_34](https://user-images.githubusercontent.com/24418024/150837452-7840ba04-d941-406e-9db6-32c04d933f5a.png)

And enter your credentials in order to connect to the database.

![Screenshot_35](https://user-images.githubusercontent.com/24418024/150837787-84a62281-ab6b-4900-921b-24b174982eb7.png)


###### Step 5

Run the ```main.py``` file in order to begin the process and create the Fact Table and the Dimensions!

###### Step 6 (Optional)

If for some reason you want to run a process by itself, you can do it in their perspective files.
eg. If you want to run the etl process, you have to run the ```etl.py``` file.


# THE END
