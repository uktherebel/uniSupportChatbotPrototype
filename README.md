_Written by @sukjinder 
_
# UniSupport System

## 1. System Description

Our system is centered around an AI-powered chatbot assistant that students can converse with about wellbeing-related
matters. The chatbot responds to students' messages with personalized wellbeing information tailored to their specific
circumstances, using the information on which it has been trained and relevant information extracted from a 'knowledge
base' containing wellbeing resources provided by the university. The other key features are a booking system for
students to make appointments with wellbeing staff and an analytics dashboard for wellbeing officers to track trends in
chats.

The purpose of our system is to address the bottlenecks faced by university wellbeing services, as well as access to
resources being fragmented and impersonal. University wellbeing services currently face a number of challenges:

- Students must wait a long time to get a response to their queries
- Wellbeing staff spend most of their time responding to individual queries about frequently asked topics
- There is little scope for wellbeing departments to systematically track data related to students' wellbeing queries

By funneling students' wellbeing queries through a chatbot, our system:

- Allows for students to get instant responses
- Frees up the time of wellbeing staff
- Enables the capturing and analysis of data related to students' wellbeing queries

## 2. Project Execution Instructions

### Setup

- Open "main.py"
- Install the packages listed in "requirements.txt" by running `pip install -r requirements.txt` in the terminal; wait
  until all packages are installed before proceeding

### Run System & Login

- Run "main.py" once all packages are installed
- Login to the system
- You can login in as the various types of users by using the email addresses below (please note that all passwords are
  set to "password" to make your experience using the prototype as convenient as possible):

**Student User**

- alee@example.com
- rpatel@example.com
- jchen@password.com

**Wellbeing Staff User**

- dcohen@example.com
- lgarcia@example.com
- mjones@example.com

**Wellbeing Manager User**

- jsmith@example.com
- kthomas@example.com
- sbaker@example.com

### Using System Features via Menu

Once successfully logged in, select an option from the menu to use the system's features (please note that the menu
options will vary based on what type of user is logged in).

Student User can:

- Start a chatbot session to talk through queries and access booking appointment system
    - Please note: the chatbot takes a few seconds to respond to messages, and you should only enter a message when '
      User: ' appears in the console
    - You can end the chat with the chatbot at any point by typing 'exit' as your message and pressing enter
- Manage their appointments
- View their notifications

Wellbeing Staff User can:

- Manage their appointments
- Manage the chatbot knowledge base
- View their notifications

Wellbeing Manager User can:

- Access the analytics dashboard and produce graphs

All of the features listed in '4. Summary of implemented functionalities' are directly accessible via the menu that
appears once you log in, with the exception of how a Student books an Appointment with a member of the Wellbeing Staff:

- This is done by a Student indicating in a message to the chatbot that they would like to book an appointment, e.g. 'I
  would like to book an appointment' (the chatbot may also suggest to the Student that they book an appointment)
- Once the Student then confirms to the chatbot that they would like to schedule such an appointment, the appointment
  booking system will appear directly in the console allowing for a Student to select an appointment to book

## 3. List of Programming Languages, Frameworks, and Tools Used

### Programming Languages

- Python

### Frameworks

- Pytest
- Singleton design pattern (appointment booking system)
- Publisher / subscriber design pattern (appointment notification system)

### Key Tools

- DeepSeek Large Language Model API
- PyTorch & Sentence Transformers packages
- Matplotlib package (Library)

## 4. Summary of Implemented Functionalities

### Chatbot

- Ability for Students to start a chat session with the chatbot and discuss wellbeing-related queries with it
    - Please note: the chatbot takes a few seconds to respond to messages, and you should only enter a message when '
      User: ' appears in the console
    - You can end the chat with the chatbot at any point by typing 'exit' as your message and pressing enter
- Ability for Wellbeing Staff to view, add or delete resources from the chatbot's knowledge base
- Ability for chatbot to initiate the appointment booking system

### Appointment Booking

- Ability for Students to book an appointment with Wellbeing Staff via the chatbot interface, by the Student indicating
  to the chatbot that they would like to schedule such an appointment
- Ability for Students & Wellbeing Staff to cancel previously booked appointments
- Ability for Students & Wellbeing Staff to view notifications related to appointments

### Analytics

- Ability for Wellbeing Managers to view summary data on system usage over time and common topics Students discuss with
  the chatbot
- Ability for Wellbeing Managers to export data to csv file

### Design Patterns

- Singleton design pattern is used for the appointment booking system class - this ensures there's only one appointment
  list being used and updated at one time
- Publisher / subscriber design pattern is used for the appointment notification system in the appointment booking
  system class - this ensures wellbeing staff are notified when a student is added to the waiting list

### Class Relationships

These include, but are not limited to:

- Inheritance from the User class (parent) and the Student, WellBeingStaff and WellbeingManager classes (children)
- Association between the chatbot class and the appointment booking system class

### Test Cases

Test cases for each feature can be found in the tests folder. Run the .py file in each folder to run both the positive
and negative test cases for that feature.

## 5. Team Contribution Percentages and Specific Work Done

| Name                    | Contribution | Work Done                                                                                                                |
|-------------------------|--------------|--------------------------------------------------------------------------------------------------------------------------|
| Andrew Cashmore         | 20%          | Appointment booking system; appointment booking system testing; chatbot testing; analytics system testing                |
| Sukjinder Dhaliwal      | 20%          | Chatbot; app & feature integration; app menu; project management                                                         |
| Usama Khalid            | 20%          | Appointment booking system; appointment booking system testing; system models (users, appointments, notifications, etc.) |
| Nabeel Shaheen          | 20%          | Analytics system                                                                                                         |
| Leonidas Theodoropoulos | 20%          | Chatbot; knowledge base; chatbot testing; video editing                                                                  |
