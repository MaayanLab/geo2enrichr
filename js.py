import os
from builder import PROBE2GENE


def js():
	js = open('../../g2e/web/extension/common/js/platforms.js', 'w+')
	js.write('// This file is built when new platforms are added.')
	js.write('//')
	js.write('// We use an array rather than hitting an API endpoint because this is much')
	js.write('// faster. If the server is too slow, we will not notify the user that the')
	js.write('// platform is not supported in a timely fashion.')


def grunt():
	os.system('grunt --gruntfile=/Users/gwg/g2e/scripts/gruntfile.js build')


if __name__ == '__main__':
	js()
	grunt()
