# api_gateway

Edge rate limiting for all public endpoints (**ADR-003**).

`nginx.conf` defines a `limit_req_zone` that drops abusive traffic at the gateway,
before it reaches a Django worker. This is the *only* place rate limiting is enforced.

Application code (Django middleware, DRF `throttle_classes`, `@ratelimit` decorators)
must **not** implement rate limiting — see [ADR-003](../docs/adr/ADR-003-gateway-rate-limiting.md).
