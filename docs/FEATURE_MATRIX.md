# Feature Matrix

Legend: **A** explicitly supported, **B** strongly implied, **C** reconstruction decision, **D** inconsistent/excluded.

| Feature | Class | Evidence / decision |
|---|---:|---|
| Email/password registration and login | A | Sprint 1 registration/profile; authentication throughout report |
| JWT authentication and session expiry | A | Sprint 2 architecture and retrospectives |
| Google/GitHub social login | B | Sprint 1 test-case screenshot only; extension point, not baseline |
| MFA | B | One Sprint 2 bullet; not consistently evidenced |
| Password reset | A | Sprint 2 user story and functional test |
| User profile | A | Sprint 1 feature and backlog |
| Financial profile | A | Income, expenses, savings, goals, risk tolerance explicitly named |
| Rule-based entity chatbot | A | Results section design 1 |
| AI intent/entity chatbot | A | Results section design 2 |
| Sentiment-aware delivery | B | Sprint 1 goal; deferred extension |
| Personalized finance insights | A | Abstract and sprint functional documents |
| Budget/savings/investing/retirement education | A | Abstract and interactive-session examples |
| Deterministic metrics | C | Safe reconstruction of personalized insight requirements |
| Dashboard | A | Sprint 2 feature |
| Query/conversation history | A | Sprint 2 and 3 user stories/tests |
| Search across financial content | A | Sprint 1 enhanced search feature |
| MongoDB persistence | A | Sprint 2 schema and connection-monitoring references |
| User-managed MongoDB connections | D | Copied backend-as-a-service schema; unsafe and unrelated |
| Admin/user/guest roles | A | Authorization matrices across sprints |
| Email notification and history | A | Sprint 3 goals/features/tests |
| Cloudinary file storage | A | Sprint 3 goals/features/tests |
| Mock provider fallbacks | C | Enables credential-free local execution and testing |
| Bank transactions/transfers/withdrawals | D | Mentioned only in generic architecture; no coherent user flow; unsafe |
| Stripe integration | D | Secret appears in copied schema only |
| Per-user SMTP/Cloudinary credentials | D | Unsafe copied connection schema |
| Live market data/top-performing stocks | D | No authoritative provider or reproducible evidence |
| Courses and skill-sharing marketplace | D | Directly conflicts with title, abstract, finance requirements/results |
| Peer video sessions, quizzes, forums | D | Learning-platform residue |
| Microservices, queues, serverless | D | Aspirational terminology; modular monolith selected |
| Gemini RAG over an income-tax PDF | B | Appendix screenshots show experimental notebook; not a complete requirement |
| Evaluation of both chatbot designs | A | Results chapter comparison; reconstructed as reproducible benchmark |

