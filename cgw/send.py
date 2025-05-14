# -*- coding: utf-8 -*-

import sys
import os
from libtssemail import Smtp

dir = os.path.dirname(sys.argv[0])
addr = sys.argv[1]
subj = sys.argv[2]

images = file(os.path.join(dir, 'images.txt')).read().splitlines()
body = file(os.path.join(dir, 'body.txt')).read()

sender = Smtp('no-reply@sevenseals.ru', 'no-reply@sevenseals.ru', 'z6854124', 'smtp.yandex.ru', 587)
result_msg = sender.send('TSS GSM Mail Server', [addr], subj, '', body, images, [])

sys.exit(len(result_msg) != 0)
