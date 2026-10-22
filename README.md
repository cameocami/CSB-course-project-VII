# Basic Poll App 
This is the course project for [Introduction to Cyber Security](https://cybersecuritybase.mooc.fi/) [part VII](https://cybersecuritybase.mooc.fi/module-3.1). The project is a basic poll web application, that will contain 5 different flaws from the [OWASP top ten list (2021)](https://top10.owasp.org/2021/) and their fixes.

## Security Flaws
### FLAW 1: [Broken Access Control](https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/)
#### Links pinpointing the flaw
- front-end: code starts [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html) & ends [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html)
- back-end: code starts [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py) & ends [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py)
#### Description
Voting is supposed to be limited to logged in users, but with current set up anonymous users can vote despite not being logged in. The html form just hides the submission button as seen [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html), which can easily be edited back into the form via browser developer tools. In addition, the back-end voting function defaults to the first user in the database as seen [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py). 
#### How to fix it
Comment out code between these two comments in the back-end:
```
"""
FLAW 1: Broken Access Control starts here
"""
"""
FLAW 1: Broken Access Control ends here
"""
```
which can be found [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py). 

In addition comment out html between 
```
<!--FLAW 1 Broken Access Control starts here-->
```
```
<!--FLAW 1 Broken Access Control ends here-->
```
which can be found [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html). 

Meanwhile, comment back in the solution under:
```
FLAW 1 Broken Access Control solution
```
which is [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py). And in the frontend:
```
FLAW 1: Broken Access Control solution
```
which can be found [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html). 

The solution adds the decorator @login_required to the back-end voting method and doesn't use a default user. The front-end checks user authentication before rendering the form, and displays a list of the choices for an anonymous user. 
#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-1.png) The flaw in its organic state.
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-2.png) The flaw with the hidden attribute of submission button removed.
- [3](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-3.png) Successful vote with anonymous user. 
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-after-1.png) Webapp with the flaw patched.

### FLAW 2: [Cryptographic Failures](https://top10.owasp.org/2021/A02_2021-Cryptographic_Failures/)

#### Links pinpointing the flaw
- [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py)

#### Description
Passwords should be stored and sent in an indecipherable format, but with current set up admins can view stored passwords in database in a plaintext format.

#### How to fix it
Comment out code
```
"""
FLAW 2: Cryptographic Failures starts here
"""
PASSWORD_HASHERS = [ "polls.dummyhasher.DummyHasher" ]
"""
FLAW 2: Cryptographic Failures ends here
"""
```
which again is [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py). 

Django will fall back on its default password hashers. 

#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-before-1.png) User creation & login (alice:redqueen) using only dummy password hashing. 
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-before-2.png) Password saved in database in format: {hasher name} $ {salt} $ {plaintext password}.
- [3](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-before-3.png) Admin view of user details. 
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-1.png) User creation & login (bob:thedragqueen) using default hashing. 
- [5](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-2.png) Password saved in database in format: {hasher name} $ {salt} $ {hashed password}.
- [6](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-3.png) Admin view of user details. 

### [Injection](https://top10.owasp.org/2021/A03_2021-Injection/)
### [Identification and Authentication Failures](https://top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures/)
### [Security Logging and Monitoring Failures](https://top10.owasp.org/2021/A09_2021-Security_Logging_and_Monitoring_Failures/)
