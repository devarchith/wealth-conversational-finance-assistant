# API Specification

Base URL: `/api`. JSON is the default media type. Protected routes require `Authorization: Bearer <JWT>`.

| Method | Route | Access | Purpose |
|---|---|---|---|
| GET | `/health` | Public | Service/database/provider health |
| POST | `/auth/register` | Public | Create user and send mock/real confirmation |
| POST | `/auth/login` | Public | Obtain JWT |
| GET | `/auth/me` | User | Current user |
| POST | `/auth/logout` | User | Acknowledge client-side JWT disposal |
| POST | `/auth/password-reset/request` | Public | Always return a neutral response |
| POST | `/auth/password-reset/confirm` | Public | Consume an expiring reset token |
| GET/PUT | `/profile` | User | Read/update user profile |
| GET/PUT | `/financial-profile` | User | Read/update financial profile |
| GET | `/recommendations` | User | Metrics and explainable recommendations |
| POST | `/chat/rule-based` | User | Deterministic finance chatbot |
| POST | `/chat/ai` | User | AI/mock intent-and-entity chatbot |
| GET | `/history` | User | Paginated conversations |
| GET | `/history/{conversation_id}` | Owner | Conversation and messages |
| DELETE | `/history/{conversation_id}` | Owner | Delete owned conversation/messages |
| POST | `/storage/upload` | User | Validated optional upload |
| GET | `/notifications/history` | User | User's notification events |
| GET | `/admin/summary` | Admin | Privacy-limited counts/provider status |

## Chat contract

Request:

```json
{"message":"How can I improve my emergency fund?","conversation_id":null}
```

Response:

```json
{
  "response":"...",
  "intent":"emergency_fund",
  "entities":["emergency fund"],
  "confidence":0.92,
  "engine":"rule_based",
  "conversation_id":"...",
  "disclaimer":"Educational information, not professional financial advice."
}
```

## Error model

Errors use an HTTP status appropriate to the failure and `{ "detail": "human-readable message" }`. Authentication requests avoid revealing whether an email is registered where enumeration would create risk.

