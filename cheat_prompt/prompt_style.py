"""Styles for the cheat prompt, pop up menu, toolbar."""

from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


class PromptStyle(Style):
    """Prompt style updates the default style with custom colors."""

    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#282828 #cc241d',
        Token.Menu.Completions.Completion: 'bg:#504945 #ebdbb2 bold',
        Token.Toolbar: '#fe8019 bg:#1d2021',
        Token.PromptText: '#fe8019',
        Token.PromptSymbol: '#458588',
    }
    styles.update(DefaultStyle.styles)
