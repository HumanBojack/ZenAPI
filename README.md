# ZenApi
## Context
ZenApi is part of the [ZenApp project](https://github.com/yayahamour/ZenApp). The main application needed to **communicate with an API** in order to **access the database**.

## Technologies
The idea was to have **a database** and **an API** communicating inside of a **Docker container**, which we could easily deploy (in our case, to azure).

### The database
We used **postgresql**, mainly because we are familiar with it and it was easy to deploy as a container.

In the database, we have two tables :
- **user** => Containing informations about the user such as:
	- *username* (string, primary_key)
	- *first_name* (string)
	- *last_name* (string)
	- *is_admin* (bool)
- **dailytext** => Containing users' texts:
	- *id* (integer, primary_key)
	- *text* (text)
	- *date* (date)
	- *emotion* (string)
	- *user_username* (foreign_key)

### The API
We also used **FastAPI** because of it's **simplicity** and the previous experiences we had with it.

In the API, we have various methods to make a **CRUD** on the **user** and **dailytext** tables. The api is also used to **classify text** with the help of the model each day at noon.
