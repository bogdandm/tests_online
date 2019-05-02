from django.urls import reverse


def get_auth_headers(client, **credentials) -> dict:
    """

    :param client: Django test client
    :param credentials: Credentials for auth request
    :return: Headers dict
    """
    resp = client.post(reverse('token_obtain_pair'), data=credentials)
    tokens = resp.json()
    return {'HTTP_AUTHORIZATION': f'Bearer {tokens["access"]}'}
