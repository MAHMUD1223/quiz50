# Quiz50

#### Video Demo: [Quiz50 Demo](https://youtu.be/KNhOcFS_MMo?si=08UyK1rTyQ5t0Wtt)

#### Description:

Quiz50 is a versatile and engaging quiz web application designed to cater to both quiz enthusiasts and creators. This platform empowers users to create, share, and participate in quizzes, making it an excellent tool for both entertainment and education. Whether you're looking to test your knowledge, challenge friends, or share your expertise with others, Quiz50 provides a user-friendly and feature-rich environment to do so. One of the standout features of Quiz50 is its robust user management system. Users can easily register, log in, and manage their profiles. The application allows users to change their usernames and passwords, ensuring that they can maintain the security and uniqueness of their accounts. This level of user management is crucial for creating a personalized and secure experience. Quiz50 is built entirely on the Flask framework, a lightweight and powerful web framework for Python. Flask provides the flexibility and simplicity needed to develop and maintain web applications efficiently. The application leverages SQLite3 as its database, ensuring a reliable and straightforward data management solution. By using Object Relational Mapping (ORM), Quiz50 ensures that database interactions are both convenient and secure, reducing the risk of SQL injection attacks and other common database vulnerabilities. The application also incorporates Flask-Migrate, a powerful tool for handling database migrations. This feature allows developers to apply and manage database schema changes seamlessly, ensuring that the application can evolve and adapt to future requirements without compromising data integrity. Flask-Migrate adds a layer of flexibility and security, making it easier to implement updates and improvements. A dynamic ranking system is integrated into Quiz50, providing users with a competitive edge. As users participate in quizzes and earn points, the ranking system updates in real-time, reflecting their performance and encouraging continuous engagement. This gamification element enhances the overall user experience, motivating users to participate more actively. Quiz50 is not just about playing quizzes; it's also about knowledge sharing. Users can create their quizzes on various topics, contributing to a diverse and ever-growing repository of quizzes. This collaborative aspect of Quiz50 fosters a community of learners and educators, where knowledge can be shared and discovered.

### Features:

- **User Management**: Quiz50 includes advanced user management features. Users can easily change their usernames and passwords through the account settings.
- **Flask Framework**: The application is entirely based on Flask, a lightweight and powerful Python web framework.
- **Database**: It uses SQLite3 as the database. The integration of Object Relational Mapping (ORM) ensures convenient and secure database access and updates.
- **Database Migrations**: With Flask-Migrate, the application can handle future database updates flexibly and securely, minimizing the risk of data loss.
- **Ranking System**: There is a dynamic ranking system that updates continuously based on the points earned by users through quizzes. This adds a competitive edge and encourages continuous participation.
- **Knowledge Sharing**: Users can sharpen their knowledge by playing quizzes or contribute by creating new ones.
###### How To Host The application
Just get the src files form project dir and follow the instructions
- Create a virtual environment
```bash
python -m venv env
```
- Change to env
```bash
source env/bin/activate
```
- Install dependencies
```bash
pip install -r requirements.txt
```
- Start the app
```bash
python app.py
```
>[!NOTE]
> I used `python app.py` insted of `flask run` because it will host the app to all ip and will make debugging possible if wanna host it somewhere just use production WSGI server insted as this way it will be more secure that `python app.py` or `flask run`

###### How to create a account in quiz50
Just simply navigate to `/register` You will be given a resguster form and you just need to fill that up. Note that username is unique so you must choose a unique username and strong minmum 8 char long password.
>[!NOTE]
> This application does not require any email address so everyone can it without email. So, please don't do anything sameful.
##### Conclusion
Quiz50 offers a robust platform for both quiz enthusiasts and creators. With its advanced features and user-friendly design, it provides an excellent tool for learning and sharing knowledge. Whether you're looking to test your skills or challenge your friends, Quiz50 is the perfect place to do it. Enjoy creating and playing quizzes, and see how you rank among other users!

That's all.
This was cs50.
