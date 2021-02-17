This is an referal app in which user can login or signup.
Logged  in users can generate referal code and share via email.
If new user sign up with this referal code, both gets 100 points.

This is done using django and docker-compose.
So you need to install docker and docker-compose in your machine.

Once the branch is checkedout, follow below command

docker-compose up
in new tab-
docker exec -it django bash
 python manage.py makemigrations
 python manage.py migrate

For sending emails, change the email address and put your password in the below file.
Referal_log_APP/referal/sendemail.py

Thats it go to localhost:8000
