# Blog API (proxy) - Django + DRF + Clean-ish Architecture

This project provides a small Django REST API that proxies requests to the external CodeLeap careers endpoints (as specified). It uses a layered structure approximating Clean Architecture:
- repositories/: HTTP calls to the external API (lowest-level infrastructure)
- services/: business/use-case logic
- serializers/: DTO validation
- views/: controllers (DRF APIViews)
- tests/: unit tests that mock external calls

Included features:
- Create, list, update, delete endpoints for posts
- Swagger UI (drf-yasg)
- Unit tests with pytest (mocks external HTTP calls)
- All code commented to explain design choices

## Requirements

Create a virtualenv and install dependencies from requirements.txt (Python 3.10+ recommended).

## Run locally (step-by-step)

1. Create virtualenv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt