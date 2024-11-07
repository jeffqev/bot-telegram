import { HandleStartCommand, HandleHelpCommand, HandleMessage } from "../src/handler";

describe("Test Commands", () => {
  it("start handler should be return the message with name", () => {
    const name = "John";
    const result = HandleStartCommand(name);
    expect(result).toBe(
      `Hello ${name}! Please enter the expense you want to add.`
    );
  });

  it("help handler should be return the help message", () => {
    const result = HandleHelpCommand();
    expect(result).toBe('The available commands are:\n/start\n/help');
  });

  it("message handler should be return the message", () => {
    const result = HandleMessage("Hello");
    expect(result).toBe("Hello");
  });

  it("message handler should be return the message", () => {
    const result = HandleMessage("/error");
    expect(result).toBe('Unrecognized command.');
  });
}
)
