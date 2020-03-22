def join_urls(first_url, second_url):
    if not first_url:
        return second_url

    if not second_url:
        return first_url

    first_url = first_url.strip("/")
    second_url = second_url.lstrip("/")

    return "/".join([first_url, second_url])
