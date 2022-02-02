from flask import url_for, current_app
from flask_mail import Message
from locationApp import mail

def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request',
                recipients=[user.email])
  msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
  try:
    mail.send(msg)
  except Exception as e:
    raise e