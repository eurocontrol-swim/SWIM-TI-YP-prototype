"""
Copyright 2019 EUROCONTROL
==========================================

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the 
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following 
   disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
   disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products 
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE 
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

==========================================

Editorial note: this license is an instance of the BSD license template as provided by the Open Source Initiative: 
http://opensource.org/licenses/BSD-3-Clause

Details on EUROCONTROL: http://www.eurocontrol.int
"""
import os
import sys
import hashlib
import yaml
from getpass import getpass

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

__author__ = "EUROCONTROL (SWIM)"

MIN_PASSWORD_LENGTH = 10


def _get_input_method():
    """
    Distinguish python versions and return the input method for raw input
    :return: callable
    """
    try:
        return __builtins__.raw_input
    except AttributeError:
        return input


def get_pwned_password_range(password_sha1_prefix):
    """
    Retrieves a range of sha1 pwned passwords from haveibeenpwned API whose 5 first characters match with the provided
    sha1 prefix.

    :param password_sha1_prefix: must be 5 characters long
    :type
 str    :return: list of str
    """
    response = urlopen('https://api.pwnedpasswords.com/range/{0}'.format(password_sha1_prefix))
    data = str(response.read())

    if response.code not in [200]:
        raise ValueError(data)

    return [str(passwd) for passwd in data.split('\\r\\n')]


def password_has_been_pwned(password):
    """
    Chacks if the provided password has been pwned by querying the haveibeenpwned API

    :param password:
    :type: str
    :return: bool
    """
    password_sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    password_sha1_prefix = password_sha1[:5]

    pwned_password_suffixes = get_pwned_password_range(password_sha1_prefix)

    full_pwned_passwords_sha1 = [password_sha1_prefix + suffix[:35] for suffix in pwned_password_suffixes]

    return password_sha1 in full_pwned_passwords_sha1


def is_strong(password, min_length=MIN_PASSWORD_LENGTH):
    """
    Determines whether the password is strong enough using the following criteria:
    - it does not contain spaces
    - its length is equal or bigger that max_length
    - it has been pwned before (checked via haveibeenpwned API)

    :param password:
    :type: str
    :param min_length:
    :type: int
    :return: bool
    """
    return ' ' not in password \
        and len(password) >= min_length \
        and not password_has_been_pwned(password)


class User:

    def __init__(self, id, description, username, password):
        """
        :param id:
        :type: str
        :param description:
        :type: str
        :param username:
        :type: str
        :param password:
        :type: str
        """
        self.id = id
        self.description = description
        self.username = username
        self.password = password


def _load_config(filename):
    """

    :param filename:
    :type: str
    :return: dict or None
    """
    with open(filename) as f:
        obj = yaml.load(f, Loader=yaml.Loader)

    return obj or None


def _prompt_for_user(user):
    """

    :param user:
    :type: User
    :return: User
    """
    input_method = _get_input_method()

    sys.stdout.write('\n{0}\n'.format(user.description))
    user.username = input_method(" username [{0}]: ".format(user.username)) or user.username
    user.password = getpass(prompt=" password: ")

    while not is_strong(user.password):
        sys.stdout.write('The password is not strong enough. Please try again.\n')
        user.password = getpass(prompt=" password: ")

    return user


def main():

    if len(sys.argv) != 3:
        sys.stdout.write("Usage: python3 main.py </path/to/config_file> </path/to/output_file>\n")
        exit(1)

    config_file, output_file = sys.argv[1], sys.argv[2]

    if not os.path.exists(config_file):
        sys.stdout.write("Invalid config_file\n")
        exit(1)

    config = _load_config(config_file)

    if config is None:
        sys.stdout.write("Error while loading config file\n")
        exit(0)

    users = [User(id=user_id,
                  description=data.get('description'),
                  username=data.get('default_user'),
                  password=None)
             for user_id, data in config['USERS'].items()]

    users = [_prompt_for_user(user) for user in users]

    with open(output_file, 'w') as f:
        for user in users:
            f.write('{0}_USER={1}\n'.format(user.id, user.username))
            f.write('{0}_PASS={1}\n'.format(user.id, user.password))


if __name__ == '__main__':
    main()
