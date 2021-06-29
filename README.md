# MVP
Application to manage the product 

 # Steps to Project Setup 
 
 <p> clone the repostiry onto your local machine using the following command. </p>


```bash
git clone https://github.com/madanpandey97/MVP.git

```

Create a virutal env on your system, navigate into the project folder and install the pip dependancy using following command.

```bash
pip install -r requirements.txt

```

# Step to run the project

**Note ---- I have not used any external database here, only the default database sqlite is being used here so no need for additional database installation**

to run the migration, run the following command in order.

```bash
python manage.py makemigrations 
python manage.py migrate
```
I have made a management command to load the dummy data into sqlite3 database, run the following command to load the data.

```bash
python manage.py general_data
```