# Basic Poll App 
This is the course project for [Introduction to Cyber Security](https://cybersecuritybase.mooc.fi/) [part VII](https://cybersecuritybase.mooc.fi/module-3.1). The project is a basic poll web application, that will contain 5 different flaws from the [OWASP top ten list (2021)](https://top10.owasp.org/2021/) and their fixes.

## Security Flaws
### FLAW 1: [Broken Access Control](https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/)
#### Links pinpointing the flaw
- front-end: [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html#L38) 
- back-end: [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py#L83)
#### Description
Voting is supposed to be limited to logged in users, but with current set up anonymous users can vote despite not being logged in. The html form just hides the submission button, which can easily be edited back into the form via browser developer tools. In addition, the back-end voting function defaults to the first user in the database.

#### How to fix it
In [views.py](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py), remove the comment delimiter for line [86](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py#L86):

```
@login_required(login_url="/login/")
```
and line [92]((https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/views.py#L92):
```
return HttpResponseRedirect(reverse('polls:login'))
```
In the [detail.html](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html#L38) template, remove the code between the comments "FLAW 1 Broken Access Control flaw starts here" and "FLAW 1 Broken Access Control flaw ends here":
```
<!--FLAW 1 Broken Access Control flaw starts here-->

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
{% endfor %}
{% if user.is_authenticated %} <input type="radio" name="choice" value="other">Other: <input type="text" name="new_choice" /> {% endif %}
<br>
<input {% if not user.is_authenticated %} hidden {% endif %} type="submit" value="Vote">
</form>
<br>
<a href="{% url 'polls:results' question.id %}">Results</a>

<!--FLAW 1 Broken Access Control flaw ends here-->
```
While removing the comment delimiters from the [code above it](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/detail.html#L13): 
```
<!--
FLAW 1 Broken Access Control solution
...
-->
```

The solution adds the decorator @login_required to the back-end voting method and doesn't use the default user. The front-end checks user authentication before rendering the form, and displays a list of the choices for an anonymous user instead of the voting form.
#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-1.png) Poll detail view as an anonymous user. 
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-2.png) Poll detail view view source code shows hidden button for form submission. 
- [3](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-before-3.png) Successful vote with anonymous user. 
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-1-after-1.png) Fixed: Poll detail view as an anonymous user.

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
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-1.png) Fixed: User creation & login (bob:thedragqueen) using default hashing. 
- [5](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-2.png) Fixed: Password saved in database in format: {hasher name} $ {salt} $ {hashed password}.
- [6](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-2-after-3.png) Fixed: Admin view of user details. 

### FLAW 3: [Injection](https://top10.owasp.org/2021/A03_2021-Injection/)
#### Links pinpointing the flaw
- [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/results.html)
#### Description
User input should be by default considered not trust-worthy. Current set up labels user input as safe in the html template, which will cause the the browser to render it as is. Only a simple pop-up is scripted for this demonstration, but the inline JavaScript could eg. a function that would send the session cookie to an external server.
#### How to fix it
Navigate to the results.html page [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/polls/templates/polls/results.html). Comment out the html between these two comments:
```
<!--FLAW 3 Injection flaw starts here-->
<li>{{ choice.choice_text | safe }} -- {{ choice.get_votes }} vote{{ choice.votes|pluralize }}</li>
<!--FLAW 3 Injection flaw ends here-->
```
Meanwhile, comment back in the solution :
```
<!--FLAW 3 solution
<li>{{ choice.choice_text }} -- {{ choice.get_votes }} vote{{ choice.votes|pluralize }}</li>
-->
```
The solution removes the safe filter from the html template. Now the template will automatically escape characters could be interpreted by the browser. For example, the character "&" is converted to "&amp".
#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-3-before-1.png) User input of malicious code.
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-3-before-2.png) User input posted. Redirect to results pages shows user input rendered as is. 
- [3](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-3-before-3.png) Browser executes malicious code and creates the pop-up when navigating to results page. 
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-3-before-4.png) Snap shot of the unescaped user input in the html-file.
- [5](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-3-after-1.png) Fixed: Diplay of results & html with the user input escaped. 
### FLAW 4: [Identification and Authentication Failures](https://top10.owasp.org/2021/A07_2021-Identification_and_Authentication_Failures/)

#### Links pinpointing the flaw
- [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py)

#### Description
Weak, well-known passwords should not be permitted. Current set up bypasses Django provided password validation, so that users can sign up using weak and/or commonly known passwords. This leaves the program open to authentication-related attacks.
#### How to fix it
Comment back in:
```
"""
FLAW 4: Identification and Authentication Failures starts here
# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
FLAW 4: Identification and Authentication Failures ends here
"""
```
which again is [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py). 

Program will validate the passwords before user creation. It will check for minimum length, only numeric passwords, and similarity of the password to the username. In addition it will check againts this common password [list](https://gist.github.com/roycewilliams/226886fd01572964e1431ac8afc999ce) of 20,000 common passwords created by Royce Williams. 

#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-4-before-1.png) User creation without password validation.  
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-4-before-2.png) Successful user creation using weak credentials (username:password).
- [3](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-4-before-3.png) Successful login using weak credentials (username:password).
- [4](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-4-after-1.png) Fixed: User creation with password validation.   
- [5](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-4-after-2.png) Fixed: User creation unsuccessful using weak credentials (username:password).  

### FLAW 5: [Security Logging and Monitoring Failures](https://top10.owasp.org/2021/A09_2021-Security_Logging_and_Monitoring_Failures/)

#### Links pinpointing the flaw
- [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py)

#### Description
Client-side should not be able to view error message details. The current set-up send full details to client when error occurs. 

#### How to fix it
Change debug setting from True to False:
```
DEBUG = True
```
which again is [here](https://github.com/cameocami/CSB-course-project-VII/blob/main/mysite/mysite/settings.py). 

Program will show standard error page according to HTTP response status code.  
#### Screenshots
- [1](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-5-before-1.png) Poll not found 404 error message with full log.  
- [2](https://github.com/cameocami/CSB-course-project-VII/blob/main/screenshots/flaw-5-after-1.png) Fixed: Poll not found 404 error message with minimal information.
