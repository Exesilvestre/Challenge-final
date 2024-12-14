const API_URL = 'http://localhost:5000'; // Cambiar cuando tengas el backend listo.

export const fetchConversations = async () => {
  const response = await fetch(`${API_URL}/conversations`);
  return response.json();
};

export const fetchMessages = async (conversationId) => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}/messages`);
  return response.json();
};

export const sendMessage = async (conversationId, message) => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text: message }),
  });
  return response.json();
};
