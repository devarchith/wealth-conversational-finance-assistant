import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import ChatPage from "./page";

const apiMock = vi.fn();
vi.mock("@/lib/api", () => ({ api: (...args: unknown[]) => apiMock(...args) }));
vi.mock("@/components/Protected", () => ({ Protected: ({children}:{children:React.ReactNode}) => children }));

describe("ChatPage", () => {
  it("switches assistant modes and uses a suggested prompt", () => {
    render(<ChatPage/>);
    fireEvent.click(screen.getByRole("radio", {name:/Rule-Based/i}));
    expect(screen.getByText("Rule engine active")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", {name:/How healthy is my monthly cash flow/i}));
    expect(screen.getByLabelText("Your finance question")).toHaveValue("How healthy is my monthly cash flow?");
  });

  it("renders a readable assistant answer with optional details", async () => {
    apiMock.mockResolvedValueOnce({response:"Your reported surplus is positive.",intent:"cash_flow",engine:"mock_ai",entities:[],confidence:.94,conversation_id:"conversation-1",disclaimer:"Educational information."});
    render(<ChatPage/>);
    fireEvent.change(screen.getByLabelText("Your finance question"), {target:{value:"How is my cash flow?"}});
    fireEvent.click(screen.getByRole("button", {name:"Send question"}));
    await waitFor(() => expect(screen.getByText("Your reported surplus is positive.")).toBeInTheDocument());
    expect(screen.getByText("Why this answer")).toBeInTheDocument();
  });
});
