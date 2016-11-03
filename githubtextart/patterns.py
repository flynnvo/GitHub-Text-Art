# Copyright 2016 Flynn van Os
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

patterns = {
    'A' : [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
    'B' : [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
    'C' : [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
    'D' : [[1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0]],
    'E' : [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
    'F' : [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
    'G' : [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
    'H' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
    'I' : [[1], [1], [1], [1], [1], [1], [1]],
    'J' : [[0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
    'K' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 0], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1]],
    'L' : [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]],
    'M' : [[1, 0, 0, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1]],
    'N' : [[1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]],
    'O' : [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
    'P' : [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]],
    'Q' : [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]],
    'R' : [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1]],
    'S' : [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1]],
    'T' : [[1, 1, 1, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]],
    'U' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]],
    'V' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [0, 1, 1, 0]],
    'W' : [[1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 1, 0, 1], [0, 1, 1, 1, 0]],
    'X' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1]],
    'Y' : [[1, 0, 0, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [1, 1, 1, 1]],
    'Z' : [[1, 1, 1, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 1, 1, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 1, 1]]
}

def check_text_length(text):
    """Ensure the user-entered text fits in GitHub's contributions history view"""
    length = 0
    possible = ''
    for character in text:
        length += len(patterns[character][0]) + 1
        if(length > 53):
            print('Input text too long!')
            print('Maximum achievable:', possible)
            return False
        possible += character
    return True

def get_start_date():
    """Get the first date to start drawing on the contribution graph.

    This date is the start of the first full week on the GitHub contribution graph.
    This is given by the first Sunday after the date one year ago.
    """
    one_year_ago = datetime.today() - relativedelta(years = 1)

    one_year_ago += relativedelta(days = (6 - one_year_ago.weekday()))
    one_year_ago = one_year_ago.replace(microsecond=0)
    return one_year_ago

def get_draw_dates(text):
    """Get a list of all the dates needed to commit to create the text in the contribution graph"""
    start_date = get_start_date()
    draw_dates = []
    for letter in text:
        if letter is ' ':
            start_date += timedelta(weeks = 2)
            continue
        draw_date = start_date
        letter_pattern = patterns[letter]
        character_width = len(letter_pattern[0])
        for row in letter_pattern:
            draw_date = start_date
            for item in row:
                if item == 1:
                    date_iso_text = draw_date.isoformat() + 'Z'
                    draw_dates += [date_iso_text]
                draw_date += timedelta(weeks = 1)
            start_date += timedelta(days = 1)
        start_date += timedelta(weeks = character_width)
    return draw_dates
