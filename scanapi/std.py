

class response:

    # ${{ std:response.status_is(200) }}
    def status_is(code: int, *, response) -> bool:
        return response.status_code == code

    # ${{ std:response.status_in_range(200, 204) }}
    def status_in(*codes: int, response) -> bool:
        return response.status_code in codes

    # ${{ std:response.status_in_range(200, 299) }}
    def status_in_range(start: int, end: int, *, response) -> bool:
        return response.status_code in range(start, end)

    # ${{ std:response.ok }}
    def ok(response) -> bool:
        return response.status_code in range(200, 300)
