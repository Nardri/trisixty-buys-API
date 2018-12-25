"""Module for all constants"""

CHARSETS = ['utf-8', 'ascii']
EXCLUDES = ['password', 'deleted']

MESSAGES = {
    'DUPLICATES':
    'duplicate error: {} already exists.',
    'CREATED':
    '{} successfully created.',
    'REGISTER':
    'You have successfully registered, please check '
    'your email to verify your account.',
    'LOGIN':
    'You have successfully logged in.',
    'UNAUTHORIZED':
    'Sorry you do not have the correct credentials, please '
    'try again with the correct details.',
    'ERROR':
    'An error occurred',
    'REQUIRED_FIELDS':
    'Field is required and cannot be less than three '
    'character.',
    'NOT_FOUND':
    'Oops!, Sorry we could not find you on our system.',
    'EMAIL_FORMAT':
    'You have entered an invalid email.',
    'INVALID_PASSWORD':
    'Password must be alphanumeric and must contain at least one special character.',
    'PROCEED_TO_LOGIN':
    '{}, please proceed to login.',
    'VERIFIED':
    'Email already verified',
    'NOT_VERIFIED':
    'You need to verify your account',
    'EXPIRED_TOKEN':
    'Unfortunately, this verification token has expired',
    'RESEND_EMAIL':
    'Your verification email have been resent.',
    'INVALID_EMAIL':
    'You have provided an invalid email',
    'RESET_LINK':
    'A reset link have been sent to your email.',
    'RESET_LINK_RESEND':
    'Please resend the reset link.'
}

EXCEPTIONS = {
    'EMAIL_ERROR':
    'An error occurred while trying to send the email.',
    'CONNECTION_ERROR':
    'An error occurred while trying '
    'to connect to the email server.'
}
