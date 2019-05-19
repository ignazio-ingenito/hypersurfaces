import sys

from webapp.models import init_db
from webapp.seed import Seed

if __name__ == '__main__':

    if 'db' in sys.argv:
        init_db()
        Seed().run()
    else:
        print('Invalid argument')
        print('Available options\n')
        print('db - intial database setup')
