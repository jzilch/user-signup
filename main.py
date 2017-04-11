#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

def valid_username(username):
    return username and re.compile(r"^[a-zA-Z0-9_-]{3,20}$").match(username)

def valid_password(password):
    return password and re.compile(r"^.{3,20}$").match(password)

def valid_email(email):
    return email and re.compile(r"^[\S]+@[\S]+.[\S]+$").match(email)

#html header code
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User-Signup</title>
</head>
<body>
    <h1>Signup</h1>
"""

#html footer code
page_footer = """
</body>
</html>
"""

user_signup = """
<form action="/" method="post">
    <label>
        Username
        <input type="text" name="username" value="%(uservalue)s" value required>
        <span style="color:red">%(user-error)s</span>
    </label><br>
    <label>
        Password
        <input type="password" name="password" value required>
        <span style="color:red">%(password-error)s</span>
    </label><br>
    <label>
        Verify Password
        <input type="password" name="verify" value="" value required>
        <span style="color:red">%(verify-error)s</span>
    </label><br>
    <label>
        Email (optional)
        <input type="text" name="email" value="%(emailvalue)s">
        <span style="color:red">%(email-error)s</span>
    </label><br>
    <input type="submit">
</form>
"""

congrats = """
<h1>Welcome, %(username)s!</h1>
"""
content = page_header + user_signup + page_footer
congrats_page =  congrats + page_footer


class MainHandler(webapp2.RequestHandler):

    def WriteForm(self, usererror, passworderror, verifyerror, emailerror, username, email):
        self.response.out.write(content % {"user-error": usererror,
                                           "password-error": passworderror,
                                           "verify-error": verifyerror,
                                           "email-error": emailerror,
                                           "uservalue": username,
                                           "emailvalue": email })

    def get(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        usererror = ''
        passworderror = ''
        verifyerror = ''
        emailerror = ''
        self.WriteForm(usererror, passworderror, verifyerror, emailerror, username, email)

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if valid_username(username):
            usererror = ''
        if not valid_username(username):
            usererror = "That's not a valid username"
            have_error = True

        if valid_password(password):
            passworderror = ''
        if not valid_password(password):
            passworderror = "That wasn't a valid password"
            have_error = True

        if password != verify:
            verifyerror = "That wasn't the same password"
            have_error = True
        if password == verify:
            verifyerror = ''

        if email == '':
            emailerror = ''
        else:
            if valid_email(email):
                emailerror = "That's not a valid email"
                have_error = True

        if have_error == True:
            self.WriteForm(usererror, passworderror, verifyerror, emailerror, username, email)

        if have_error == False:
            self.redirect("/congratulations?username=" + username)



class Congratulations(MainHandler):
    def WelcomeUser(self, username):
        self.response.out.write(congrats_page % {'username': username})

    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.WelcomeUser(username)
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/congratulations', Congratulations)
], debug=True)
