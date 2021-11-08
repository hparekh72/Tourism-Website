# Toursim Website

A tourism website made using Django where Admin can
create,update,delete tour packages and Users can book a
tour package.

https://tripology.herokuapp.com/



## Tech Stack

• Html

• CSS

• Javascript

• Bootstrap

• Django

• PostgreSQL

  
## Features

- Admin can create,update,delete new tour packages and users 
- Register/Login using Email Verification
- Forget Password using Email Verification
- Search tour packages 
- View itinerary of tour package 
- Booking tour packages (On Booking, an Email will also be sent to the user regarding booking details)
- Canceling a tour package
- Adding testimonials





  
## Deployment

To deploy this project run

```bash
  python manage.py runserver
```

For Email Verification to work:

Step 1: Enabling less secure apps to access Gmail

Step 2:
In settings.py file of telusko folder

    EMAIL_HOST_USER = 'Enter Your Email over here'
    EMAIL_HOST_PASSWORD = 'Enter Your Password over here '
