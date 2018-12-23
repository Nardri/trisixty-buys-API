"""Module for all constants"""

CHARSETS = ['utf-8', 'ascii']
EXCLUDES = ['password', 'deleted']

MESSAGES = {
    'DUPLICATES':
    'duplicate error: {} already exists.',
    'CREATED':
    '{} successfully created.',
    'LOGIN':
    'You have successfully logged in.',
    'UNAUTHORIZED':
    'Sorry you do not have the correct credentials, please '
    'try again.',
    'ERROR':
    'An error occurred',
    'REQUIRED_FIELDS':
    'Field required and cannot be less than three '
    'character.',
    'NOT_FOUND':
    'Oops!, am sorry we cannot find you on our system.',
    'EMAIL_FORMAT':
    'Please provide a valid email.'
}
