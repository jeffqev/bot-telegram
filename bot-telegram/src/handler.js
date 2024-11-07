export function HandleStartCommand(name) {
  return `Hello ${name}! Please enter the expense you want to add.`;
}

export function HandleHelpCommand() {
  return 'The available commands are:\n/start\n/help';
}

export function HandleMessage(msg) {
  if (msg.startsWith('/')) {
    return 'Unrecognized command.';
  }
  return msg;
}