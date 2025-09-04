"""
Service (use-case) layer: coordinate input validation and repository calls.

Keeping business rules here makes views thin and easy to test.
""" 
from .repositories import external

def list_posts(params=None):
    # Directly forwards query parameters to repository.  
    return external.list_posts(params=params)

def create_post(validated_payload):
    # Any business-level enrichment or validation would happen here.
    return external.create_post(validated_payload)

def update_post(pk, validated_payload):
    return external.update_post(pk, validated_payload)

def delete_post(pk):
    return external.delete_post(pk)