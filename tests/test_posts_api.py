"""Unit tests for posts endpoints. We patch the repository functions to avoid real network calls."""
import json
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch

client = APIClient()

@pytest.mark.django_db
def test_list_posts_success(monkeypatch):
    sample = {'count': 1, 'results': [{'id': 1, 'username': 'u', 'title': 't', 'content': 'c'}]}
    with patch('posts.repositories.external.list_posts', return_value=sample):
        resp = client.get(reverse('posts-list-create'))
        assert resp.status_code == 200
        assert resp.json() == sample

@pytest.mark.django_db
def test_create_post_success():
    payload = {'username': 'john', 'title': 'hello', 'content': 'world'}
    created = {'id': 10, **payload}
    with patch('posts.repositories.external.create_post', return_value=created):
        resp = client.post(reverse('posts-list-create'), data=json.dumps(payload), content_type='application/json')
        assert resp.status_code == 201
        assert resp.json() == created

@pytest.mark.django_db
def test_update_post_success():
    pk = 5
    payload = {'title': 'new'}
    updated = {'id': pk, 'username': 'u', 'title': 'new', 'content': 'c'}
    with patch('posts.repositories.external.update_post', return_value=updated):
        url = reverse('posts-detail', kwargs={'pk': pk})
        resp = client.patch(url, data=json.dumps(payload), content_type='application/json')
        assert resp.status_code == 200
        assert resp.json() == updated

@pytest.mark.django_db
def test_delete_post_success():
    pk = 7
    with patch('posts.repositories.external.delete_post', return_value={}):
        url = reverse('posts-detail', kwargs={'pk': pk})
        resp = client.delete(url)
        # our view returns 204 on success
        assert resp.status_code == 204
        assert resp.content == b''