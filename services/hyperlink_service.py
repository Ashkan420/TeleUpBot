import re


def convert_hyperlinks(text: str) -> str:
    """
    Converts 'text'(link) or "text"(link) into HTML hyperlinks.
    Example: "Google"(google.com) -> <a href="https://google.com">Google</a>
    """
    pattern = r'(?:(?:"([^\"]+)")|(?:\'([^\']+)\'))\((https?://[^\s)]+|www\.[^\s)]+|[^\s)]+\.[^\s)]+)\)'

    def repl(match):
        display_text = match.group(1) if match.group(1) is not None else match.group(2)
        link = match.group(3)

        if not re.match(r'^https?://', link):
            link = 'https://' + link

        return f'<a href="{link}">{display_text}</a>'

    return re.sub(pattern, repl, text)
