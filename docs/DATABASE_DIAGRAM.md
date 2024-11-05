# Database Diagram (SQLite)

```mermaid
erDiagram
    ORDERS { string code PK; string phone; string customer; string product; int qty; int total; string status; string tracking; string eta; string created }
    SESSIONS { string id PK; string state; string pending_order; string pending_phone; int fallback_count; int handoff; string handoff_reason }
    MESSAGES { int id PK; string session_id FK; string role; string content; string intent; float confidence }
    TICKETS { int id PK; string code UK; string session_id FK; string content; string status }
    KB_ENTRIES { int id PK; string intent; string question; string answer }
    UNRESOLVED { int id PK; string session_id FK; string question }
    SESSIONS ||--o{ MESSAGES : "ghi lại"
    SESSIONS ||--o{ TICKETS : "phát sinh"
    SESSIONS ||--o{ UNRESOLVED : "phát sinh"
```

Trạng thái đơn (`orders.status`): PENDING, PACKING, SHIPPING, DELIVERED, CANCELLED, RETURNING.
Trạng thái phiên (`sessions.state`): IDLE, AWAIT_ORDER, AWAIT_PHONE.
