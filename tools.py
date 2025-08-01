#tools.py

from langchain.tools import tool

@tool
def generate_long_note(content):
    return long_note

@tool
def generate_short_note(content):
    return short_note

