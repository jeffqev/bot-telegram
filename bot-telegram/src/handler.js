import axios from 'axios';

export function HandleStartCommand(name) {
  return `Hello ${name}! Please enter the expense you want to add.`;
}

export function HandleHelpCommand() {
  return 'The available commands are:\n/start\n/help';
}

export async function HandleMessage(msg, telegram_id) {
  if (msg.startsWith('/')) {
    return '';
  }

  try {
    const response = await axios.post(
      `${process.env.BASE_API_URL}/analyze_expense`,
      { text: msg, user_id: `${telegram_id}` }
    );

    if (response.status === 200) {
      const expense = response.data.response[0];
      return `${expense.category} expense added ✅`
    }

  } catch (error) {
    if (error.response) {
      if (error.response.status === 401) {
        return `Unauthorized access for user ${telegram_id}.`;
      } else if (error.response.status === 400) {
        return '';
      }
    }
    return '';
  }

  return '';
}