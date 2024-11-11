import { jest } from '@jest/globals';
import { HandleStartCommand, HandleHelpCommand, HandleMessage } from "../src/handler";
import axios from 'axios';

axios.post = jest.fn();

describe("Test Commands", () => {
  it("start handler should return the message with name", () => {
    const name = "John";

    const result = HandleStartCommand(name);

    expect(result).toBe(
      `Hello ${name}! Please enter the expense you want to add.`
    );
  });

  it("help handler should return the help message", () => {
    const result = HandleHelpCommand();

    expect(result).toBe('The available commands are:\n/start\n/help');
  });

  it("message handler should return the empty message for unrecognized command", async () => {
    const result = await HandleMessage("/error", "12345");

    expect(result).toBe('');
  });

  it("message handler should return the expense added message when status is 200", async () => {
    const mockResponse = {
      status: 200,
      data: {
        response: [{ category: "Food" }],
      },
    };
    axios.post.mockResolvedValue(mockResponse);

    const result = await HandleMessage("Pizza 20 dollars", "12345");

    expect(result).toBe("Food expense added ✅");
  });

  it("message handler should return unauthorized message when status is 401", async () => {
    const mockResponse = {
      response: {
        status: 401
      }
    };
    axios.post.mockRejectedValue(mockResponse);

    const result = await HandleMessage("Pizza 20 dollars", "12345");

    expect(result).toBe('Unauthorized access.');
  });

  it("message handler should return empty message when status is 400", async () => {
    const mockResponse = {
      response: {
        status: 400
      }
    };
    axios.post.mockRejectedValue(mockResponse);

    const result = await HandleMessage("Pizza 20 dollars", "12345");

    expect(result).toBe('');
  });
});