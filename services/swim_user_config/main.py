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
from typing import List, Optional, Dict, Union, Any
from urllib.request import urlopen
from getpass import getpass


__author__ = "EUROCONTROL (SWIM)"

MIN_PASSWORD_LENGTH = 10


def get_pwned_password_range(password_sha1_prefix: str) -> List[str]:
    """
    Retrieves a range of sha1 pwned passwords from haveibeenpwned API whose 5 first characters match with the provided
    sha1 prefix.

    :param password_sha1_prefix: must be 5 characters long
    :return:
    """
    with urlopen(f'https://api.pwnedpasswords.com/range/{password_sha1_prefix}') as response:
        data = str(response.read())

        if response.code not in [200]:
            raise ValueError(data)

        return [str(passwd) for passwd in data.split('\\r\\n')]


def password_has_been_pwned(password: str) -> bool:
    """
    Chacks if the provided password has been pwned by querying the haveibeenpwned API

    :param password:
    :return:
    """
    password_sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    password_sha1_prefix = password_sha1[:5]

    pwned_password_suffixes = get_pwned_password_range(password_sha1_prefix)

    full_pwned_passwords_sha1 = [password_sha1_prefix + suffix[:35] for suffix in pwned_password_suffixes]

    return password_sha1 in full_pwned_passwords_sha1


def is_strong(password: str, min_length: Optional[int] = MIN_PASSWORD_LENGTH) -> bool:
    """
    Determines whether the password is strong enough using the following criteria:
    - it does not contain spaces
    - its length is equal or bigger that max_length
    - it has been pwned before (checked via haveibeenpwned API)

    :param password:
    :param min_length:
    :return:
    """
    return ' ' not in password \
        and len(password) >= min_length \
        and not password_has_been_pwned(password)


class User:

    def __init__(self, id: str, description: str, username: str, password: Union[str, None]):
        self.id = id
        self.description = description
        self.username = username
        self.password = password


def _load_config(filename: str) -> Union[Dict[str, Any], None]:
    """

    :param filename:
    :return:
    """
    with open(filename) as f:
        obj = yaml.load(f, Loader=yaml.Loader)

    return obj or None


def _prompt_for_user(user: User) -> User:
    """

    :param user:
    :return:
    """
    print(f'\n{user.description}')
    user.username = input(f" username [{user.username}]: ") or user.username
    user.password = getpass(prompt=f" password: ")

    while not is_strong(user.password):
        print('The password is not strong enough. Please try again:')
        user.password = getpass(prompt=f" password: ")

    return user


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 main.py </path/to/config_file> </path/to/output_file>")
        exit(1)

    config_file, output_file = sys.argv[1], sys.argv[2]

    if not os.path.exists(config_file):
        print("Invalid config_file")
        exit(1)

    config = _load_config(config_file)

    if config is None:
        print("Error while loading config file")
        exit(0)

    users = [User(id=user_id,
                  description=data.get('description'),
                  username=data.get('default_user'),
                  password=None)
             for user_id, data in config['USERS'].items()]

    users = [_prompt_for_user(user) for user in users]

    with open(output_file, 'w') as f:
        for user in users:
            f.write(f'{user.id}_USER={user.username}\n')
            f.write(f'{user.id}_PASS={user.password}\n')


if __name__ == '__main__':
    main()
