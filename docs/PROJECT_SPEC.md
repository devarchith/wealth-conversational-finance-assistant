# Reconstructed Project Specification

## Status and evidence model

This specification reconstructs the intended **Wealth Conversational Finance Assistant** from the final university report. It is not a claim that the new code is the byte-for-byte original implementation. Statements are tagged as report evidence, reconstruction assumptions, or modern implementation decisions.

## Objective

Build a secure, accessible finance-education application that uses natural-language conversations and a user's financial profile to explain budgeting, savings, emergency funds, risk, diversification, investing basics, goals, and retirement planning. Calculations are deterministic; AI is used only for interpretation and educational explanation.

## Target users and roles

- **Users:** students, professionals, retirees, novice investors, and financially experienced individuals (report evidence).
- **User role:** owns a private profile, financial profile, chats, recommendations, history, and uploads.
- **Admin role:** may inspect aggregate service health and user/account status without receiving plaintext credentials or unrestricted finance data.
- **Guest:** may view public educational material and landing pages; cannot access personal data.

## Core capabilities

### Authentication and sessions

- Email/password registration and login, secure password hashing, JWT access tokens, current-user lookup, and client-side logout.
- Password-reset request and completion with expiring, single-use reset tokens and mock/SMTP delivery.
- Role-based authorization for user and admin endpoints.
- The report mentions social login and MFA in screenshots/text, but neither is consistently specified. Extension points are documented; local authentication is the reconstructed baseline.

### User and financial profiles

- User profile: display name, preferred currency, timezone, financial-literacy level, optional avatar URL.
- Financial profile: monthly income, monthly expenses, current savings, intended monthly investment, financial goals, risk tolerance, and investment horizon.
- No bank login, card number, brokerage secret, or financial-institution credential is stored.

### Finance chatbot and NLP

- **Rule-based engine:** preprocessing, finance entity extraction, intent patterns, deterministic response selection, confidence, and fallback. It intentionally remains less capable with complex negation/multiple intents while staying usable.
- **AI engine:** `AIProvider` abstraction with a working mock implementation and an optional OpenAI-compatible provider. It returns response, intent, entities, confidence, and engine metadata.
- Covered domains: budgeting, savings, expenses, emergency funds, stocks, mutual funds, retirement, risk, diversification, basic investing, and financial goals.
- Both modes are educational and must not promise returns, execute trades, or fabricate live market prices.

### Recommendations and dashboard

- Deterministic metrics: monthly surplus, savings rate, expense ratio, emergency-fund target and gap, goal progress, and basic risk-profile classification.
- Dashboard: key metrics, financial-goal progress, risk profile, personalized recommendations, and recent conversations.
- Recommendations are heuristics with transparent formulas and limitations, not individualized professional advice.

### History

- Conversations and messages are persisted with user ownership, engine, intent, entities, confidence, and timestamps.
- Paginated list, conversation detail, and delete endpoints strictly scope queries by authenticated user.

### Notifications, email, and storage

- `EmailProvider`: mock and SMTP implementations for registration confirmation, password reset, and account notices; email history stores delivery metadata, never SMTP secrets.
- `StorageProvider`: mock/local-metadata and Cloudinary implementations for optional profile images or finance-document metadata. The app works without Cloudinary credentials.
- File types and sizes are validated; uploaded content is not treated as trusted instructions.

### Admin

- Admin-only service summary, user count, conversation count, provider modes, and health signals.
- Admin does not receive password hashes, reset tokens, provider secrets, or unrestricted user message content.

## Explicit exclusions

- Skill-sharing marketplace, courses, peer tutoring, quizzes, forums, gamification, and video lessons are inconsistent with the finance product and excluded.
- Bank transfers, withdrawals, purchases, portfolio execution, Stripe payment processing, live bill payment, and brokerage integration are not sufficiently justified and create unacceptable risk.
- Per-user MongoDB/SMTP/Cloudinary secrets are rejected. Service credentials belong in deployment environment variables.
- Real-time stock recommendations and market-price claims are excluded without a configured authoritative market-data provider.

## Testing expectations

- Backend tests cover authentication, authorization, profiles, chatbot modes, metrics, history isolation, reset tokens, provider fallback, mock email/storage, validation, and admin boundaries.
- Frontend validation includes lint, TypeScript checking, component/unit coverage for important behavior, and a production build.
- Evaluation compares rule-based and mock/AI engines using labeled queries and reports only measured results.

