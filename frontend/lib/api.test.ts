import { describe, expect, it } from "vitest";
import { clearToken, formatMoney, formatPercent, getToken, setToken } from "./api";

describe("client utilities",()=>{
 it("stores and clears the access token",()=>{setToken("abc");expect(getToken()).toBe("abc");clearToken();expect(getToken()).toBeNull();});
 it("formats metrics without inventing unavailable rates",()=>{expect(formatPercent(0.256)).toBe("26%");expect(formatPercent(null)).toBe("Not available");expect(formatMoney(1200,"USD")).toContain("1,200");expect(formatMoney(1200,"NOT-A-CURRENCY")).toContain("1,200");});
});
