# ShopSphere — Monolithic E-commerce Learning Roadmap
### (Amazon/Flipkart-style features, ek single FastAPI backend ke andar — Microservices nahi)

**Core Learning Principle:** Har technology sirf "use karne ke liye" nahi seekhi jayegi — pehle ek real production problem create hogi, phir uska solution ban kar concept clear hoga. Fark sirf itna hai ki iss baar sab kuchh **ek hi codebase / ek hi app** ke andar `modules/` ki tarah organize hoga (e.g. `app/auth`, `app/orders`, `app/payments`) — koi separate service, API Gateway, ya inter-service Kafka event-bus nahi.

**Stack:** Python, FastAPI, Pydantic, SQLAlchemy, Alembic, PostgreSQL, Redis, Celery, Elasticsearch (optional advanced), Docker (single/compose), Pytest.

**Kya jaan-bujh kar hata diya hai:** separate services per domain, API Gateway, Kafka as inter-service event backbone, Saga/Outbox pattern (distributed-transaction fixes), Kubernetes, multi-service CQRS/analytics pipeline. In sab ki jagah normal Postgres transactions (ACID) aur in-app function calls use honge — jo ek monolith mein sahi aur simpler approach hai.

---

## PHASE 1 — Project Foundation & Auth
**Problem:** Users ko securely register/login karana hai, aur social login ("Login with Google") bhi chahiye.
**Concepts:** FastAPI project structure (modular, not microservice), JWT access + refresh token, password hashing (bcrypt), RBAC (CUSTOMER/ADMIN/SELLER), OAuth2 login (Google), OpenAPI docs.
**Deliverable:** `app/auth` module — signup/login/refresh/logout + Google login working.

## PHASE 2 — User Profile & Session Continuity
**Problem:** Login hone par user ka last browsing state (recently viewed, filters) restore hona chahiye.
**Concepts:** Data modelling (address/preferences), Redis-backed session cache keyed by `user_id`.
**Deliverable:** `app/users` module + "Recently Viewed" persisting across logout/login.

## PHASE 3 — Product Catalog & Search
**Problem:** Simple `LIKE %query%` search slow/limited hai — typo par kuchh nahi milta, filters combine karna mushkil.
**Concepts:** Product CRUD in Postgres; Elasticsearch/OpenSearch for fuzzy + faceted search (advanced add-on); index sync via a scheduled/background job (no Kafka needed — direct DB→ES sync script or Celery task).
**Deliverable:** `app/products` — catalog + fast/fuzzy/faceted search API.

## PHASE 4 — Cart (Redis-backed, persistent)
**Problem:** Cart sirf frontend mein rahe to doosre device par khali milta hai.
**Concepts:** Cache-aside pattern, write-through persistence to Postgres, guest-cart merge on login.
**Deliverable:** `app/cart` — same cart across devices after login.

## PHASE 5 — Wishlist & Recently Viewed
**Problem:** Users apne pasand ke products baad mein dekhna chahte hain.
**Concepts:** Redis sorted sets (time-ordered), TTL-based expiry, dedup.
**Deliverable:** `app/wishlist` — add/remove + recently-viewed carousel API.

## PHASE 6 — Order Module
**Problem:** Order banate waqt product validate, price calculate, coupon apply — sab ek jagah coordinate karna.
**Concepts:** Order state machine (PENDING → CONFIRMED → PAID → SHIPPED → DELIVERED → CANCELLED); ek hi DB transaction ke andar sab related writes (no distributed coordination needed since it's one database).
**Deliverable:** `app/orders` — end-to-end order creation with correct status transitions.

## PHASE 7 — Payment Integration
**Problem:** Duplicate requests double-charge kar sakte hain; webhooks blindly trust karna risky hai.
**Concepts:** Idempotency keys (Redis), payment intent flow, webhook signature verification, refund handling. (Stripe/Razorpay test mode — yeh ek real external API hai, isliye retry/timeout concepts yahin naturally aayenge.)
**Deliverable:** `app/payments` — idempotent payment API.

## PHASE 8 — Inventory & Concurrency
**Problem:** Do customers ek saath last item order kar dete hain — dono ko "confirmed" mil jaata hai.
**Concepts:** `SELECT FOR UPDATE` row locking, optimistic locking (version column), Redis distributed lock as alternative.
**Deliverable:** `app/inventory` — race-condition-free stock decrement.

## PHASE 9 — Coupon & Flash-Sale
**Problem:** Flash sale mein 1000 log ek saath "Buy Now" dabate hain, stock sirf 50 — overselling risk.
**Concepts:** Business rule validation, Redis atomic `DECR`, per-user rate limiting.
**Deliverable:** `app/coupons` — flash-sale endpoint jo kabhi oversell na kare.

## PHASE 10 — Review & Rating
**Problem:** Fake reviews trust kharab karte hain.
**Concepts:** Verified-purchase check, rating aggregation, moderation queue.
**Deliverable:** `app/reviews` — reviews + average star rating API.

## PHASE 11 — Recommendation Engine
**Problem:** Generic listing engagement kam karti hai.
**Concepts:** Simple collaborative filtering (offline job with pandas/numpy), precomputed recommendation cache in Redis.
**Deliverable:** `app/recommendations` — "Related products" API.

## PHASE 12 — Shipping & Tracking
**Problem:** Order ke baad customer ko real-time package location pata honi chahiye.
**Concepts:** Third-party courier API integration (Shiprocket/Delhivery test mode), status webhooks updating the same order record directly.
**Deliverable:** `app/shipping` — "Track Order" API.

## PHASE 13 — Return & Refund
**Problem:** Return aane par refund + stock restore + status update — sab consistent hona chahiye.
**Concepts:** Ek hi DB transaction ke andar refund-trigger + inventory-restore + status-update (monolith mein yeh straightforward hai — no Saga/compensation pattern needed).
**Deliverable:** `app/returns` — return flow jo refund + stock restore + status update karta ho.

## PHASE 14 — Seller / Vendor Module
**Problem:** Multiple sellers apne products list karte hain, sirf apna data dekh sakne chahiye.
**Concepts:** Multi-tenancy via `seller_id` scoping in Postgres, seller-level RBAC.
**Deliverable:** `app/sellers` — add product, view own orders/sales.

## PHASE 15 — Invoice Generation
**Problem:** Order complete hone ke baad downloadable invoice chahiye.
**Concepts:** Server-side PDF generation (ReportLab/WeasyPrint), object storage (S3/MinIO), async generation via Celery.
**Deliverable:** `app/invoices` — real PDF download.

## PHASE 16 — Notifications (Email / SMS / Push)
**Problem:** Order lifecycle ke har stage par sahi channel par update chahiye.
**Concepts:** Trigger notifications directly from order-status-change code (function call, not event bus), template rendering, channel fallback, Celery for async send.
**Deliverable:** `app/notifications` — email/SMS/push sab order-events par fire ho.

## PHASE 17 — Redis, Beyond Caching
**Problem:** Product reads DB ko slow kar rahe hain; APIs abuse ho sakti hain; race conditions.
**Concepts:** Cache-aside, cache invalidation, sliding-window rate limiting, distributed locks, OTP/session storage — sab ek jagah revisit karke consolidate.
**Deliverable:** Consolidated Redis usage across cache, rate-limit, lock, session, cart.

## PHASE 18 — Celery Background Jobs
**Problem:** Email, invoice, reports, cleanup — request ko slow nahi karna chahiye.
**Concepts:** Task queue, worker, broker (Redis), scheduled/periodic tasks (Celery Beat).
**Deliverable:** Notifications, invoices, reports — sab async Celery tasks ke through.

## PHASE 19 — Admin & Sales Analytics
**Problem:** Business ko sales/traffic data chahiye bina production DB ko heavy queries se load kiye.
**Concepts:** Read-replica ya separate analytics schema/materialized views, scheduled aggregation jobs (Celery Beat) — same DB, no separate pipeline needed.
**Deliverable:** Admin dashboard API — today's sales, top products, revenue by category.

## PHASE 20 — Resilience Patterns (for external calls only)
**Problem:** Payment gateway, courier API, SMS provider — yeh **external** services down/slow ho sakte hain.
**Concepts:** Timeout, exponential-backoff retry, circuit breaker, idempotency — specifically applied to outbound calls to third-party APIs (not needed between your own modules, since it's one process/one DB transaction).
**Deliverable:** Payment/shipping/SMS calls jo external failure ko gracefully handle karein.

## PHASE 21 — Testing Strategy
**Concepts:** Unit tests (pytest), integration tests (real DB/Redis), API/contract tests, end-to-end tests (signup → order → payment → notification).
**Deliverable:** Test suite covering all modules above.

## PHASE 22 — Docker
**Problem:** App + Postgres + Redis + (optional) Elasticsearch ko manually chalana painful hai.
**Concepts:** Dockerfile for the single app, `docker-compose.yml` for app + Postgres + Redis, volumes, env-based config.
**Deliverable:** `docker-compose up` se pura ShopSphere ek command se chal jaaye.

## PHASE 23 — Observability, Security & CI/CD
**Problem:** Production mein slow/insecure requests pata chalne chahiye, deployment automated honi chahiye.
**Concepts:** Structured logging, basic tracing (OpenTelemetry — optional), Prometheus + Grafana metrics, OWASP basics (input validation, CORS, rate limiting, HTTPS, secrets in `.env`/Vault), GitHub Actions CI/CD, semantic versioning, branching (`main`/`develop`/`feature/*`), Conventional Commits.
**Deliverable:** Monitored, secured, CI/CD-deployed ShopSphere monolith.

---

## Security Checklist (har module mein follow karna)
- Passwords hamesha bcrypt/argon2 se hash
- JWT access token expiry chhota (15–30 min), refresh token rotate
- Har input Pydantic se validate; ORM parameterized queries (SQL injection safe)
- CORS sirf trusted origins ke liye
- Rate limiting login/OTP endpoints par
- Payment webhook signature hamesha verify
- Secrets kabhi Git mein commit nahi — `.env` / GitHub Secrets
- HTTPS/TLS har jagah
- Dependencies regularly scan (Dependabot/pip-audit)

## How to Use
- Ek time par sirf ek phase — agla phase tabhi shuru karo jab current phase ka module chal raha ho.
- Har phase se pehle uska "Problem" padho, phir solution seekho.
- Naya concept aaye to khud chhota experiment likh kar test karo (e.g. do parallel requests bhej kar race condition reproduce karo).
- Phase 22 (Docker) tak agar Docker environment available nahi hai to sirf code/architecture develop karo, baad mein containerize kar lena.

Service:
auth-service

Container:
shopsphere-auth

Database container:
shopsphere-auth-db

Database:
shopsphere_auth

Volume:
auth_postgres_data

Application port:
8001

Container port:
8000

PostgreSQL host port:
5434

PostgreSQL container port:
5432