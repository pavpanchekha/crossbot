# file name cannot be random because we need to import it
import crossbot

from crossbot.parser import date_fmt

import datetime
import random

def init(client):

    parser = client.parser.subparsers.add_parser('random', help='random mini crossword url')
    parser.set_defaults(command=random_date_url)

    parser.add_argument(
        '--start-date',
        default = first_dt,
        type    = crossbot.date,
        help    = 'Date to get times for.')

    parser.add_argument(
        '--end-date',
        default = 'now',
        type    = crossbot.date,
        help    = 'Date to get times for.')

mini_url = "https://www.nytimes.com/crosswords/game/mini/{:04}/{:02}/{:02}"

first_date = '2014-08-21'
first_dt = datetime.datetime.strptime('2014-08-21', date_fmt)

def random_date_url(client, request):

    start = request.args.start_date
    end   = request.args.end_date

    if type(start) is str:
        start = datetime.datetime.strptime(start, date_fmt)
    if type(end) is str:
        end = datetime.datetime.strptime(end, date_fmt)

    if start > end:
        request.reply('Your dates are mixed up')
        return

    if start < first_dt:
        request.reply('That start date is too early, must be {} or later'
                      .format(first_date))
        return

    rand = start + random.random() * (end - start)

    request.reply(mini_url.format(rand.year, rand.month, rand.day))

