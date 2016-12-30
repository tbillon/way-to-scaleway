"""
SW tutorial
~~~~~~~~~~~

SW API command line
"""
import os
import sys

import wts_api
from wts_api.settings import Settings


def main():
    """Program entry point
    """
    credentials = os.environ.get('CREDENTIALS')
    if credentials is None:
        print 'Could not load credentials file'
        sys.exit(1)
    Settings.load_from_file(credentials)
    app = wts_api.start_api()
    app.run(host='0.0.0.0', port='5000')


if __name__ == '__main__':
    main()
