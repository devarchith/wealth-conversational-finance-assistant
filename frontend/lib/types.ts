export type User = { id: string; email: string; role: "user" | "admin"; created_at: string };
export type Entity = { type: string; value: string };
export type ChatReply = { response: string; intent: string; entities: Entity[]; confidence: number; engine: string; conversation_id: string; disclaimer: string };
export type Recommendation = { category: string; priority: string; title: string; explanation: string };
export type RecommendationSummary = { monthly_surplus: number; savings_rate: number | null; expense_ratio: number | null; emergency_fund_target: number; emergency_fund_gap: number; risk_profile: string; goal_progress: Array<{ id: string; name: string; progress: number; remaining: number }>; recommendations: Recommendation[] };

