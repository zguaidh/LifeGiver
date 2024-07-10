
# LifeGiver  ~ * Where your blood can save lives *

![Alt text](https://i.postimg.cc/T30dpMD6/rename-png.jpg)

Don't let fools or mosquitoes get your blood; make good use of it. Use it to save lives instead.
Welcome to LifeGiver, a platform designed to connect donors with those in need and make every drop count.

# Introduction

## The Project
Don't let fools or mosquitoes get your blood; make good use of it. Use it to save lives instead. Welcome to LifeGiver, a platform designed to connect donors with those in need and make every drop count.

[**LifeGiver**](http://3.94.213.7/) 

## The story
The idea for Life Giver was born out of a personal experience that highlighted the critical need for a reliable blood donation system. When a close family member needed an urgent blood transfusion, the struggle to find a suitable donor in time was a wake-up call. I realized that many people want to donate blood but don't know where or when they are needed most. Life Giver aims to bridge this gap by creating an efficient, user-friendly platform that connects blood donors with hospitals in need.


# Team and roles

## [ABDALLAH HASSAN](http://www.linkedin.com/in/abdallah-gamal-bb8612262)(Project manager & Full-stack)
**Role:** Project manager & Full-stack

**Contribution:**
- Updating the front end part with the Jinja code.
- Implementation of profile settings for enhanced user customization.
- Ensuring  the Integrating of backend and Frontend parts.
- Contributed to the overall design and visual appeal of the platform.
- Managing the project in terms of tasks, time management.

## [SARA ELKAAD](https://www.linkedin.com/in/sara-muhammad-24a82a318?trk=contact-info)(Frontend Developer)
**Role:** Front-End

**Contribution:**
- Frontend developmnt.
- Ensuring a responsive and intuitive user experience.
- Developping the user interface using HTML, CSS and Bootstrap.
- Implementation of test cases.
- Created the website video.


## [HABIBA ZGUAID](https://www.linkedin.com/in/habibazguaid/)(Backend Developer)
**Role:** Back-End

**Contribution:**
- Backend development.
- Creation of data models.
- Handling the database integration.
- Implementation of users Authenticiation and API endpoints.
- Implementation of Email notification features.

## Blog posts
After the development phase, we each wrote a blog post to reflect on the Lifegiver journey.

* Sara's article: (https://medium.com/@saraelakaad/alx-portfolio-project-blog-post-fb1563cb4008)
* Abdallah's article:(https://www.linkedin.com/posts/abdallah-gamal-bb8612262_activity-7216897976810545155-i35b?utm_source=share&utm_medium=member_desktop)
* Habiba's article: (https://medium.com/@zguaidhabiba/alx-portfolio-project-blog-post-33cad72cd678)


# Technologies

## Front-End

- **Bootstrap**: A front-end framework for developing responsive and mobile-first websites.
- **JavaScript**: A programming language for interactive web elements.
- **HTML5 & CSS3**: Standard technologies for structuring and styling web pages.
- **Flask**: A lightweight WSGI web application framework in Python.
- **Jinja2**: A modern and designer-friendly templating engine for Python.

## Back-End
- **Python**: A versatile and powerful programming language.
- **Flask-SQLAlchemy**: An ORM (Object Relational Mapper) for handling database interactions.
- **MySQL**: An open-source relational database management system.
- **Flask-Mail**: A Flask extension for sending emails.
- **WTForms**: A flexible forms validation and rendering library for Python.
- **Haversine**: A Python library for calculating distances between points on the Earth.
- **Flask-Login**: A user session management for Flask.

## DevOps
- **NGINX**: A high-performance web server and reverse proxy.
- **GitHub Actions**: CI/CD workflows for automated testing and deployment.
- **Datadog**: A monitoring and analytics platform for applications.

## Monitoring
- **Datadog**: Comprehensive observability platform for monitoring application performance.


## Version Control and Collaboration
- **Git**: A distributed version control system.
- **GitHub**: A platform for version control and collaborative development.

## Server and Domain
- **Linux**: The operating system for the server environment.
- **NGINX**: Used as a web server and reverse proxy for handling HTTP requests.
- **GitHub Actions**: For CI/CD workflows.

## Cloud Services
- **Name.com**: For domain registration and management.


# Installation
### (Ongoing Process)


1. Clone the repository:
    ```bash
    git clone https://github.com/zguaidh/LifeGiver.git
    cd LifeGiver
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    ```bash
    export FLASK_APP=app.py
    export FLASK_ENV=development
    export SECRET_KEY='your_secret_key'
    export GOOGLE_MAPS_API_KEY='your_google_maps_api_key'
    export MAIL_SERVER='your_mail_server'
    export MAIL_PORT='your_mail_port'
    export MAIL_USERNAME='your_mail_username'
    export MAIL_PASSWORD='your_mail_password'
    export MAIL_USE_TLS=True
    export MAIL_USE_SSL=False
    ```

5. Initialize the database:
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6. Run the application:
    ```bash
    flask run
    ```


# Usage

Welcome to LifeGiver! Here's a step-by-step guide on how you can make the most of our blood donation platform:

## For Donors:

**Sign Up:**

Create your account by signing up on our platform. Simply provide the required details and set up your personal profile.

**Find Nearby Hospitals:**

Browse through our network of hospitals and find all the hospitals nearby 30 Km drive.


**Schedule Your Donation:**

Choose your preferred date and time for the donation. Our platform provides the flexibility to schedule your appointment at your convenience.

**Receive Notifications:**

Stay informed with notifications about recent Blood Requests. 
Also our platform will send you notifications about your upcoming donation.

**Track Your Donations:**

Keep a record of all your donations. Our platform allows you to track your donation history and see the impact you've made.

## For Hospitals:

**Sign Up:**

Register your hospital on our platform by signing up. Provide the necessary details to create a comprehensive hospital profile and get your unique Barcode.

**Set Up Hospital Profile:**

Complete your hospital profile with essential information such as location, contact details, and blood donation requirements, in your Profile UI.

**Post Urgent Requests:**

Create and post urgent blood donation requests. Specify the blood type needed, the urgency.

**Post Donation Requests:**

Create and post blood donation requests. Specify the blood type needed, and wait for a notification that includes the date choosed by the donor.

**Manage Appointments:**

Schedule and manage blood donation appointments. Ensure a smooth flow of donors by organizing time slots and minimizing wait times.

**Send Notifications:**

Utilize our notification system to send messages to all nearby donors with matching blood type and inform them about the Blood request.

**Track Donation Requests:**

Keep a detailed record of all blood donation requests. Monitor the stock levels of different blood types and manage inventory effectively.
Engage with Donors:


# Contribution

We welcome contributions from the community! Please follow these steps to contribute:

1. **Fork the repository:**
    - Start by forking the LifeGiver repository to your GitHub account.

2. **Clone Your Fork:**
    - Clone the forked repository to your local machine using:
     ```bash
     git clone https://github.com/zguaidh/LifeGiver.git
     ```

3. **Create a new branch:** 
    - Create a new branch for your contribution:
    ```bash
     git checkout -b feature/your-feature
     ```

4. **Make Your Changes:**
    - Implement new features, bug fixes, or improvements. Ensure your code follows our coding standards.

5. **Commit your changes:**
     - Commit your changes with descriptive commit messages:
     ```bash
     git commit -m "Description of your changes"
     ```

6. **Push to the branch:**
    - Push your changes to your forked repository:
     ```bash
     git push origin feature/your-feature
     ```
7. **Create a new Pull Request:**
    - Open a pull request on the LifeGiver repository. Clearly describe your changes, including any relevant context or issues.

8. **Review and Merge:**
   - LifeGiver team will review your contribution. Once approved, it will be merged into the main branch.

# Discover the Project
## ScreenShots



## Demo

<a href="https://www.youtube.com/watch?v=kpgRsQjKGEU&t=6s" target="blank">
<p align="center">Watch Website Demo</p>
<p align="center"><img width="25%" src="https://github.com/zguaidh/LifeGiver/blob/master/Lifegiver_test/lifegiver/static/images/transparent-cartoon-red-blood-blood-droplets-blood-bubbles-dar-2d-image-of-red-blood-droplets-in-bubbles658ea3c57cbf28.655540331703846853511.png" alt="lifegiver" /></p> 
</a>

# Related projects

* [AirBnB Clone]: a simple web app made in Python.

* [Simple Shell]: a command line interpreter that replicates the sh program.

# License

MIT License

Thank you for using Life Giver! Together, we can save lives by making blood donation easier and more efficient.

