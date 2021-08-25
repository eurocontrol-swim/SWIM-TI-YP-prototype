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
import hashlib
import binascii
import json
import os
import sys

__author__ = "EUROCONTROL (SWIM)"


def _get_salt() -> str:
    """
    Generates a 32bit random salt, i.e. e7663f87
    :return:
    """
    return os.urandom(4).hex()


def hash_rabbitmq_password(password: str, salt: str) -> str:
    """
    Hashes (sha256) the provided password according to the RabbitMQ algorithm

    :param salt: a 32bit string in hex, i.e. e7663f87
    :param password: any string
    :return: the hashed password
    """
    salt_and_password = salt + password.encode('utf-8').hex()

    salt_and_password_bytes = bytearray.fromhex(salt_and_password)

    salted_sha256 = hashlib.sha256(salt_and_password_bytes).hexdigest()

    password_hash = bytearray.fromhex(salt + salted_sha256)

    result = binascii.b2a_base64(password_hash).strip().decode('utf-8')

    return result


if __name__ == '__main__':
    """
    Creates the admin user provided b the user and inserts it into the definitions file
    """

    if len(sys.argv) != 4:
        print('Usage: update_definitions.py <rabbitmq_definitions_path> <broker_admin_user> <broker_admin_pass>')
        exit(1)

    _, definitions_path, broker_admin_user, broker_admin_pass = sys.argv

    if not os.path.exists(definitions_path):
        print(f'{definitions_path} does not exist.')
        exit(1)

    with open(definitions_path, 'r') as f:
        data_json = json.loads(f.read())

    data_json['users'].append(
        {
            "name": broker_admin_user,
            "password_hash": hash_rabbitmq_password(salt=_get_salt(), password=broker_admin_pass),
            "hashing_algorithm": "rabbit_password_hashing_sha256",
            "tags": "administrator"
        }
    )

    data_json['permissions'].append(
        {
            "user": broker_admin_user,
            "vhost": "/",
            "configure": ".*",
            "write": ".*",
            "read": ".*"
        }
    )

    with open(definitions_path, 'w') as f:
        f.write(json.dumps(data_json))
