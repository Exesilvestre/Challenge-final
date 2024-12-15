const API_URL = 'http://localhost:8000';

export const fetchConversations = async () => {
  const response = await fetch(`${API_URL}/conversations`);
  if (!response.ok) throw new Error('Error fetching conversations');
  return response.json();
};

export const fetchMessages = async (conversationId) => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}/messages`);
  if (!response.ok) {
    throw new Error('Failed to fetch messages');
  }
  return response.json();
};

export const sendMessage = async (conversationId, message) => {
  const response = await fetch(`${API_URL}/conversations/generate/${conversationId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ prompt: message }),
  });
  if (!response.ok) {
    throw new Error('Failed to send message');
  }
  return response.json();
};

export const createConversation = async (conversationData) => {
  const response = await fetch(`${API_URL}/conversations`, {  // Nota el endpoint correcto
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: conversationData.title })  // Enviar solo el nombre
  });
  if (!response.ok) throw new Error('Error creating conversation');
  return response.json();
};

export const updateConversation = async (conversationId, newName) => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_name: newName })
  });

  if (!response.ok) throw new Error('Error updating conversation');
  return response.json();
};

export const deleteConversation = async (conversationId) => {
  const response = await fetch(`${API_URL}/conversations/${conversationId}`, {
    method: 'DELETE',
  });

  if (!response.ok) throw new Error('Error deleting conversation');
  return response.json();
};
