#!/usr/bin/env python

from __future__ import unicode_literals
import requests
from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

__author__ = "Miroslav Vidović"

__email__ = "vidovic.miroslav@yahoo.com"
__date__ = "08.02.2017."
__version__ = "0.2"
__status__ = "Production"


class DocumentStyle(Style):  # pylint: disable=too-few-public-methods
    """
    Styles for the completion menu
    """
    styles = {
            Token.Menu.Completions.Completion.Current: 'bg:#003333 #1b9185',
            Token.Menu.Completions.Completion: 'bg:#000000 #eeeeff bold',
            Token.Menu.Completions.ProgressButton: 'bg:#003333',
            Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
            Token.Toolbar: '#ffffff bg:#333333',
            }
    styles.update(DefaultStyle.styles)


def create_autocomplete_dictionary():
    """
    Create a dictionary for autocomplete from all the files in the path
    """
    data = requests.get("http://cheat.sh/:list").text
    completion_list = data.split()
    # clist = []

    # for item in completion_list:
    #     item = item.replace("/", "")
    #     clist.append(item)

    cheat_dictionary = WordCompleter(completion_list, ignore_case=True,
            WORD=True)
    return cheat_dictionary


def main():
    """
    Use the created dictionary and activate popup on user input.
    """
    def get_bottom_toolbar_tokens(cli):
        return [(Token.Toolbar, ' Cheatsheets from http://cheat.sh. ')]

    cheat_compleater = create_autocomplete_dictionary()
    history = InMemoryHistory()

    while True:
        user_input = prompt('choose a cheatsheet> ', style=DocumentStyle,
                completer=cheat_compleater,complete_while_typing=True,
                on_abort=AbortAction.RETRY,
                get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                vi_mode=True)
        if user_input == "exit":
            break
        elif user_input == "":
            print("Please enter a cheatsheet name.")
        else:
            print('You entered:', user_input)
            cheatshet = requests.get("http://cheat.sh/"+user_input)
            print(cheatshet.text)
    print('Good Bye!')


if __name__ == '__main__':
    main()
