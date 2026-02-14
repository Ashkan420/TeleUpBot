from telegraph import Telegraph

telegraph = Telegraph()
telegraph.create_account(short_name="TeleBot")


def create_telegraph_page(title: str, author_name: str, author_url: str, html_content: str) -> str:
    response = telegraph.create_page(
        title=title,
        author_name=author_name,
        author_url=author_url if author_url else None,
        html_content=html_content
    )

    return "https://telegra.ph/" + response["path"]
