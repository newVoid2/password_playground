"""
Learning demonstration of checking passwords against known breach data using
a privacy-preserving API.

This script shows how to determine whether a password has appeared in known
data breaches by querying the Have I Been Pwned password API using a
k-anonymity based approach. Passwords are never sent over the network in
plaintext; only a partial hash prefix is transmitted, and all matching is
performed locally.

The script is intended for educational purposes to demonstrate secure API
usage, hashing, and basic security-aware design. It does not assess password
strength and is not intended for use in authentication or production systems.
"""
import requests
import hashlib
import sys


def request_api_data(query_char):
    """
    Sends a partial password hash prefix to the password breach API and
    returns the raw HTTP response.

    The function queries the Have I Been Pwned password API using the first
    five characters of a SHA-1 hash, as required by the API’s k-anonymity
    model. It reports non-success HTTP status codes and handles request
    failures gracefully without raising exceptions.

    Args:
        query_char (str): The first five characters of a SHA-1 password hash.

    Returns:
        requests.Response: The HTTP response returned by the API.
    """
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    try:
        if res.status_code != 200:
            print(f'The request failed (status code: {res.status_code}).')
    except Exception as e:
        print(f'Reguest failed while contacting the password breach API: {e}')
    return res


def breach_api_check(password):
    """
    Checks whether a password appears in known breach data using a
    privacy-preserving API lookup.

    The password is hashed locally using SHA-1 to match the format required
    by the Have I Been Pwned password API. Only the first five characters of
    the hash are sent to the API, and the remaining hash comparison is
    performed locally to avoid transmitting sensitive data.

    Args:
        password (str): The plaintext password to check for breach exposure.

    Returns:
        int: The number of times the password appears in known breaches.
    """
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


def get_password_leaks_count(hashes, hash_to_check):
    """
    Determines how many times a password hash appears in breach data returned
    by the password breach API.

    The function parses the API response body, which contains hash suffixes
    and breach counts, and compares them against the locally computed hash
    suffix. All matching is performed locally to avoid transmitting sensitive
    data.

    Args:
        hashes (requests.Response): The HTTP response containing hash suffixes
            and breach counts from the API.
        hash_to_check (str): The hash suffix to compare against the API data.

    Returns:
        int: The number of times the password appears in known breaches, or
        0 if no match is found.
    """
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def main(password):
    """
    Checks a single password against known breach data and reports the result.

    The function uses a privacy-preserving API lookup to determine whether the
    provided password appears in known breaches. It prints a factual result
    indicating whether the password was found and, if applicable, how many
    times it appears in the breach dataset.

    Args:
        password (str): The plaintext password to check for breach exposure.
    """
    count = breach_api_check(password)
    if count:
        print(
            f'{password} appears in known breach data (count: {count}).')
    else:
        print(f'{password} was not found in known breach data.')


if __name__ == "__main__":
    main(sys.argv[1])
