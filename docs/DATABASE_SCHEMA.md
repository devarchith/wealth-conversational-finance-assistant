# Database Schema

MongoDB stores application data. Secrets remain in environment variables and never appear in these collections.

## Collections

### `users`

`_id`, `email` (unique, normalized), `password_hash`, `role`, `is_active`, `created_at`, `updated_at`.

### `user_profiles`

`_id`, `user_id` (unique), `display_name`, `preferred_currency`, `timezone`, `financial_literacy`, `avatar_url`, timestamps.

### `financial_profiles`

`_id`, `user_id` (unique), `monthly_income`, `monthly_expenses`, `current_savings`, `monthly_investment`, `risk_tolerance`, `investment_horizon_months`, `goals[]`, timestamps. A goal includes `id`, `name`, `target_amount`, `current_amount`, and optional `target_date`.

### `conversations`

`_id`, `user_id`, `title`, `created_at`, `updated_at`. Index: `{user_id: 1, updated_at: -1}`.

### `messages`

`_id`, `conversation_id`, `user_id`, `role`, `content`, `engine`, `intent`, `entities[]`, `confidence`, `created_at`. Indexes enforce efficient user/conversation lookup.

### `password_reset_tokens`

`_id`, `user_id`, `token_hash` (unique), `expires_at`, `used_at`, `created_at`. Raw reset tokens are never stored.

### `notification_events`

`_id`, `user_id`, `kind`, `recipient`, `provider`, `status`, `provider_message_id`, `created_at`. No SMTP credential or message secret.

### `stored_files`

`_id`, `user_id`, `purpose`, `original_name`, `content_type`, `size`, `provider`, `public_id`, `secure_url`, `created_at`.

## Data ownership

Every personal collection includes `user_id`. API repositories query by both resource identifier and current `user_id`; admin summary endpoints return counts and health only. Delete operations use the same compound ownership filter.

## Rejected report schema

The report's `Connection` collection proposes storing MongoDB URIs, Gmail passwords, Cloudinary secrets, OAuth client IDs, and Stripe keys per user. That design is not implemented because it would create a credential vault without a justified product requirement or security model.

