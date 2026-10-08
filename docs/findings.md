# Findings: crAPI

## Finding 1: User enumeration on login

- **Test:** test_login_unknown_user (xfail)
- **What:** Login with an unregistered email returns "Given Email is not registered!". A registered email with a wrong password returns "Invalid Credentials". Both return 401, but the messages differ.
- **Risk:** Security Risk, as the hackers can easily know the given email is registered or not. Easy for phishing or password guessing. Severity : Low
- **Fix:** The return message should be "Invalid Email or Password"

## Finding 2: Phone number is not validated

- **Test:** test_signup_number_invalid_values (xfail on 4 rows)
- **What:** Signup accepts "abcdefghi", "1234,1234", "123" and "@!@#$" as a phone number (200, account created). It rejects only blank, a 300-digit value and null.
- **Risk:** The signup page accepts special characters and letters as phone numbers. Invalid values should not be stored as valid numbers, since the database 
  would then hold wrong numbers and verifying the user would not be possible. Severity: Medium
- **Fix:** Should accept only valid numbers i.e. fixed length (10 digit number), no special characters or alphabets. 

## Finding 3: Weak password policy

- **Test:** test_signup_password_weak_values (xfail)
- **What:** Signup accepts "abcdef", "123456", "password" and "qwerty123". The only rule enforced is length, 6 to 100 characters.
- **Risk:** Weak passwords are easy to guess, so an attacker can get into accounts by brute force or credential stuffing. Severity: Medium
- **Fix:** Enforce a minimum length and reject passwords found on a list of known common passwords (such as "123456" and "password").

## Finding 4: Users able to access another user's orders (BOLA)
- **Test:** test_bola_cannot_read_other_users_data (xfail)
- **What:** User B is able to access User A's order id. API used : GET /workshop/api/shop/orders/<id>
- **Risk:** The reply includes email, phone number, transaction id, payment details etc. which are sensitive user data. The order id are sequential and attacker can collect the information on all the customers.
- **Fix:** Check on the server that the order belongs to the requesting user (return 403 or 404 otherwise). 
Optionally use non-guessable ids (UUIDs) as a second layer. The xfail test turns into XPASS(strict) once fixed, which tells us to remove the marker.
- **Severity:** High

## Finding 5: Excessive data exposure in Community posts
- **Test:** test_responses_do_not_leak_sensitive_fields (xfail)
- **What:** The community posts API returns each author's email and vehicle id to any
  logged-in user, although the page only needs the nickname and picture.
  API: GET /community/api/v2/community/posts/recent (params: limit, offset)
- **Risk:** An attacker can collect the emails of all forum authors for phishing or spam.
  The vehicle id is an identifier used by other endpoints, so it helps target a specific
  user.
- **Fix:** Return only what the UI needs in the author object (nickname, profile picture).
  Never include email or vehicle id in public responses.
- **Severity:** Medium