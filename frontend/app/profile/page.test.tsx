import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ProfilePage from "./page";

const apiMock = vi.fn((path:string) => Promise.resolve(path === "/profile" ? {display_name:"Alex",preferred_currency:"USD",timezone:"UTC",financial_literacy:"beginner",avatar_url:null} : {monthly_income:5000,monthly_expenses:3200,current_savings:9000,monthly_investment:500,risk_tolerance:"moderate",investment_horizon_months:60,goals:[]}));
vi.mock("@/lib/api", async importOriginal => ({...(await importOriginal<typeof import("@/lib/api")>()),api:(...args:unknown[])=>apiMock(args[0] as string)}));
vi.mock("@/components/Protected", () => ({ Protected: ({children}:{children:React.ReactNode}) => children }));

describe("ProfilePage", () => {
  it("loads the monthly picture and lets a user add a goal", async () => {
    render(<ProfilePage/>);
    await waitFor(() => expect(screen.getByLabelText("Monthly income")).toHaveValue(5000));
    fireEvent.click(screen.getByRole("button", {name:"+ Add goal"}));
    expect(screen.getByLabelText("Goal name")).toBeInTheDocument();
    expect(screen.getByLabelText("Target amount")).toBeInTheDocument();
  });
});
