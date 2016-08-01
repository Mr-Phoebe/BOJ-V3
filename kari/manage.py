#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kari.settings")
    import django
    django.setup()

    from django.core.management import execute_from_command_line

    #execute_from_command_line(sys.argv)

    if len(sys.argv) == 2 and sys.argv[1] == 'judgefetch':
        from Core.tasks import JudgeQueue
        try:
            JudgeQueue.getJudge()
        except KeyboardInterrupt:
            JudgeQueue.release()
            print 'stop judge fetching'
    else:
        execute_from_command_line(sys.argv)

