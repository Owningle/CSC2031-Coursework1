from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import EqualTo, Length, Regexp, Required, Email, ValidationError

class ExcludedChars(object):
    """
    Errors if the field contains one of the
    passed characters.
    
    :param characters:
        String of excluded characters
        
    :param message:
        Message to display if invalid.
    """
    
    def __init__(self, chars, message=None):
        self.chars = chars
        self.message = message
        
    def __call__(self, form, field):
        chars = self.chars
        message = self.message
        
        for c in chars:
            if c in field.data:
                if message is None:
                    message = 'Invalid Characters: ' + chars
                raise ValidationError(message)

class RequiredChars(object):
    """
    Errors if the field does not contain one of the
    passed characters.
    
    :param characters:
        String of excluded characters
        
    :param message:
        Message to display if invalid.
    """
    
    def __init__(self, chars, message=None):
        self.chars = chars
        self.message = message
        
    def __call__(self, form, field):
        chars = self.chars
        message = self.message
        
        for c in chars:
            if c in field.data:
                return
        
        if message is None:
            message = 'Required Characters: ' + chars
        raise ValidationError(message)

class RegisterForm(FlaskForm):
    
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), ExcludedChars('*?!\'^+%&/()=}][{$#@<>')])
    lastname = StringField(validators=[Required(), ExcludedChars('*?!\'^+%&/()=}][{$#@<>')])
    phone = StringField(validators=[Required(), Regexp('^\d{4}-\d{3}-\d{4}$', message='Phone number must be in form XXXX-XXX-XXXX')])
    password = PasswordField(validators=[Required(), Length(min=6, max=12), Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*[ !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~])(?=.*[0-9]).*$', message='Must contain at least 1 digit, 1 lowercase, 1 uppercase and 1 special character.')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal.')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='Pin must be 32 characters long.')])
    submit = SubmitField()

class LoginForm(FlaskForm):
    
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = IntegerField()
    submit = SubmitField()