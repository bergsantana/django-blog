"""Repository layer: communicates with the external CodeLeap API.

We keep raw HTTP calls here so upper layers can be tested and replaced without touching networking code.
"""
import requests
from django.conf import settings

BASE = settings.EXTERNAL_API_BASE.rstrip('/') + '/'

class ExternalAPIError(Exception):
    pass

def list_posts(params=None):
    """GET /careers/ - returns the external API response JSON """
    resp = requests.get(BASE, params=params, timeout=10)
    if resp.status_code != 200:
        raise ExternalAPIError(f'List failed: {resp.status_code}')
    return resp.json()

def create_post(payload):
    """POST /careers/ - forward payload to external API """
    resp = requests.post(BASE, json=payload, timeout=10)
    if resp.status_code not in (200, 201):
        raise ExternalAPIError(f'Create failed: {resp.status_code} - {resp.text}')
    return resp.json()

def update_post(pk, payload):
    """PATCH /careers/:id/ - partial update """
    url = BASE + f"{pk}/"
    print(f"pk: {pk}")
    print(f"payload: {payload}          ")
    print(f"url: {url}          ")

    resp = requests.patch(url, json=payload, timeout=10)
    if resp.status_code not in (200, 204):
        print("FALHA DO STATUS CODE")
        print(resp.status_code)
        print("@#@@")
        print(resp)
        raise ExternalAPIError(f'Update failed: {resp.status_code} - {resp.text}')
    # External API returns updated object on 200, sometimes 204 with empty body
    return resp.json() if resp.text else {}

def delete_post(pk):
    """DELETE /careers/:id - delete and return {} on success """
    url = BASE + f"{pk}"
    resp = requests.delete(url, timeout=10)
    if resp.status_code not in (200, 204):
        raise ExternalAPIError(f'Delete failed: {resp.status_code} - {resp.text}')
    return {}   