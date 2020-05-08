#!/usr/bin/env python
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.utils import *
import django
import argparse
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tbot.settings")
django.setup()


def main(args):
    User = get_user_model()
    user = User.objects
    try:
        su = user.create_superuser(
            username=args.username,
            password=args.password,
            email=args.email
        )
        if su:
            print("[+] {} created.".format(args.username))
    except IntegrityError:
        print("[!] {} already exists.".format(args.username))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", default="admin",
                        help="username")
    parser.add_argument("-p", "--password", default="Passw0rd$",
                        help="password")
    parser.add_argument("-e", "--email", default="a@tbot.test",
                        help="email address")

    args = parser.parse_args()
    main(args)
