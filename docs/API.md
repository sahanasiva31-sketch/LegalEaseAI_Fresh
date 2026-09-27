# API Reference

## GET /

Returns a basic service message.

## GET /health

Returns:

```json
{
  "status": "ok",
  "service": "LegalEase API"
}
```

## POST /generate

Request:

```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": "Payment within 30 days; Confidentiality must be maintained",
  "dates": "April 15, 2025"
}
```

Response:

```json
{
  "document": "generated legal draft..."
}
```

FastAPI also provides interactive Swagger documentation at `/docs`.
