import os

def list_entries():
    """
    list all files in entries/ directory
    """
    return [f.split(".md")[0] for f in os.listdir("./entries/")]

def save_entry(title, content):
    """
    Save a file, if already exist, it will get rewrittened
    """
    f = open(f"./entries/{title}.md", "w")
    f.write(content)
    f.close()

def get_entry(title):
    """
    Retrieve an entry by its title, return None if it doesn't exist
    """
    try:
        f = open(f"./entries/{title}.md", "r")
        return f.read()
    except FileNotFoundError:
        return None