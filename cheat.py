#!/usr/bin/env python

from __future__ import unicode_literals
import requests
from prompt_toolkit import prompt, AbortAction
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.token import Token

from prompt_toolkit.key_binding.defaults import load_key_bindings_for_prompt
from prompt_toolkit.keys import Keys

from cheat_prompt.prompt_style import PromptStyle


registry = load_key_bindings_for_prompt()


def create_prompt(cli):
    """Create the prompt"""
    return [
        (Token.PromptText, 'Choose a cheatsheet '),
        (Token.PromptSymbol, '=> '),
    ] 


def create_autocomplete_dictionary():
    """
    Create a dictionary for autocomplete from all the files in the path
    """
    data = requests.get("http://cheat.sh/:list").text
    completion_list = data.split()

    cheat_dictionary = WordCompleter(completion_list, ignore_case=True,
            WORD=True)
    return cheat_dictionary

@registry.add_binding(Keys.ControlD)
def _(event):
    """
    Print 'hello world' in the terminal when ControlT is pressed.
    We use ``run_in_terminal``, because that ensures that the prompt is
    hidden right before ``print_hello`` gets executed and it's drawn again
    after it. (Otherwise this would destroy the output.)
    """
    event.cli.set_return_value("exit")

def main():
    """
    Use the created dictionary and activate popup on user input.
    """
    def get_bottom_toolbar_tokens(cli):
        return [(Token.Toolbar, ' Cheatsheets from http://cheat.sh. ')]

    cheat_compleater = create_autocomplete_dictionary()
    history = InMemoryHistory()


    while True:
        user_input = prompt(get_prompt_tokens=create_prompt, style=PromptStyle,
                completer=cheat_compleater,complete_while_typing=True,
                on_abort=AbortAction.RETRY,
                get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
                vi_mode=True,key_bindings_registry=registry)
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
