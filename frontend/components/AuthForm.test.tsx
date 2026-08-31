import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AuthForm } from "./AuthForm";

vi.mock("next/navigation",()=>({useRouter:()=>({push:vi.fn(),refresh:vi.fn()})}));

describe("AuthForm",()=>{
 it("shows reconstruction password requirements",()=>{render(<AuthForm mode="register"/>);expect(screen.getByText(/At least 10 characters/)).toBeInTheDocument();expect(screen.getByRole("button",{name:"Create account"})).toBeInTheDocument();});
 it("requires email and password inputs",()=>{render(<AuthForm mode="login"/>);const email=screen.getByLabelText("Email") as HTMLInputElement;const password=screen.getByLabelText("Password") as HTMLInputElement;fireEvent.change(email,{target:{value:"user@example.com"}});fireEvent.change(password,{target:{value:"secret"}});expect(email.value).toBe("user@example.com");expect(password.value).toBe("secret");});
});

