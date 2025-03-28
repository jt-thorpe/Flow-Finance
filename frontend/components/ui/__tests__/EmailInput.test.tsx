// EmailInput.test.tsx
import React from "react";
import { render, screen, act } from "@testing-library/react";
import EmailInput from "../EmailInput";

// A dummy register function to satisfy the prop.
const dummyRegister = jest.fn();

// Reset fake timers and mocks before and after each test.
beforeEach(() => {
  jest.useFakeTimers();
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.useRealTimers();
  jest.resetAllMocks();
});

describe("EmailInput component", () => {
  test('does not call API if email does not contain "@"', () => {
    render(<EmailInput register={dummyRegister} emailValue="invalidemail" />);
    act(() => {
      jest.advanceTimersByTime(1000); // Advance past the debounce delay
    });
    expect(global.fetch).not.toHaveBeenCalled();
  });

  test('displays "Email is already taken" error when API returns taken true', async () => {
    // Mock a successful API response with "taken" true.
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        success: true,
        taken: true,
        message: "Email is already taken",
      }),
    });

    render(<EmailInput register={dummyRegister} emailValue="taken@test.com" />);

    // Advance the timers to trigger the API call.
    await act(async () => {
      jest.advanceTimersByTime(750);
    });

    // Wait for the error message to appear.
    const errorMessage = await screen.findByText("Email is already taken");
    expect(errorMessage).toBeInTheDocument();
  });

  test("clears error when email is available", async () => {
    // Mock a successful API response with taken false.
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, taken: false }),
    });

    render(<EmailInput register={dummyRegister} emailValue="available@test.com" />);

    await act(async () => {
      jest.advanceTimersByTime(750);
    });

    // Since an empty string is falsy, no error message should be rendered.
    expect(screen.queryByText("Email is already taken")).not.toBeInTheDocument();
  });

  test("displays API error message when response is not ok", async () => {
    // Simulate an API response with an error.
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({ success: false, message: "API error" }),
    });

    render(<EmailInput register={dummyRegister} emailValue="error@test.com" />);

    await act(async () => {
      jest.advanceTimersByTime(750);
    });

    const errorMessage = await screen.findByText("API error");
    expect(errorMessage).toBeInTheDocument();
  });

  test("displays error message when fetch throws an error", async () => {
    // Simulate fetch throwing an error.
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error("Network error"));

    render(<EmailInput register={dummyRegister} emailValue="throw@test.com" />);

    await act(async () => {
      jest.advanceTimersByTime(750);
    });

    const errorMessage = await screen.findByText("Network error");
    expect(errorMessage).toBeInTheDocument();
  });
});
