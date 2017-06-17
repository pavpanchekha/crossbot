import sqlite3

import crossbot
import util

def init(subparsers):

    parser = subparsers.add_parser('announce', help='Announce any streaks.')
    parser.set_defaults(command=announce)

    parser.add_argument(
        'date',
        nargs   = '?',
        default = 'now',
        type    = util.get_date,
        help    = 'Date to announce for.')

def announce(client, args):
    '''Report who won the previous day and if they're on a streak.
    Optionally takes a date.'''

    m = ""

    with sqlite3.connect(crossbot.db_path) as con:

        def best(offset):
            offset_s = '-{} days'.format(offset)
            result = con.execute('''
            SELECT userid
            FROM crossword_time
            WHERE date = date(?, ?) AND seconds >= 0
            ORDER BY seconds ASC
            LIMIT 1''', (args.date, offset_s)).fetchone()

            return None if result is None else result[0]

        best1 = best(1)
        best2 = best(2)

        if best1 is None:
            m += 'No one played the minicrossword yesterday. Why not?\n'
        elif best1 != best2:
            # no streak
            m += 'Yesterday, {} solved the minicrossword fastest.\n'\
                 .format(client.user(best1))
            if best2 is not None:
                m += '{} won the day before.\n'\
                     .format(client.user(best2))
        else:
            n = 2
            while best(n+1) == best1: n += 1
            m += '{} is on a {}-day streak! {}\n'\
                 .format(users[best1]['name'], n, ':fire:' * n)

        m += "Play today's: https://www.nytimes.com/crosswords/game/mini"

        client.send(m)
