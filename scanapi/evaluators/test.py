def it(a: int, b: int = 0) -> int:
    return a + b

it.it = it


def off(a: int, b: int, status: str = 'x') -> int:
    return str(a) + '+' + str(b) + '-' + status


class response:

    def ok(response):
        return response.status_code < 400

    # def status_is(response, code: int):
    #     return response.status_code == code

    def status_is(code: int, response):
        return response.status_code == code
