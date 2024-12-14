import React, { useState, useEffect } from 'react';
import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import ChatWindow from '../components/ChatWindow';
import ConversationList from '../components/ConversationList';
import MessageInput from '../components/MessageInput';
import { fetchMessages, sendMessage, fetchConversations, createConversation, updateConversation, deleteConversation } from '../services/api';

const ChatPage = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newConversationTitle, setNewConversationTitle] = useState('');

  useEffect(() => {
    // Fetch real conversations from the API when the component mounts
    const loadConversations = async () => {
      try {
        const data = await fetchConversations();  // Replace with actual API call
        setConversations(data);
      } catch (error) {
        console.error("Error fetching conversations:", error);
      }
    };
    loadConversations();
  }, []);

  const handleSelectConversation = async (conversationId) => {
    setSelectedConversation(conversationId);
    try {
      const data = await fetchMessages(conversationId); // Fetch messages from the selected conversation
      setMessages(data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleSendMessage = async (text) => {
    if (selectedConversation) {
      try {
        const newMessage = await sendMessage(selectedConversation, text);
        setMessages((prev) => [...prev, newMessage]);
      } catch (error) {
        console.error("Error sending message:", error);
      }
    }
  };

  const handleOpenDialog = () => setDialogOpen(true);
  const handleCloseDialog = () => {
    setDialogOpen(false);
    setNewConversationTitle('');
  };

  const handleAddConversation = async () => {
    if (newConversationTitle.trim()) {
      try {
        const newConversation = await createConversation({ title: newConversationTitle });
        setConversations((prev) => [...prev, newConversation]);
        handleCloseDialog();
      } catch (error) {
        console.error("Error creating conversation:", error);
      }
    }
  };

  const handleEditConversation = async (id, newTitle) => {
    try {
      // Call your API to update the conversation
      const updatedConversation = await updateConversation(id, newTitle);
  
      // After the update is successful, update the conversations state
      setConversations((prev) =>
        prev.map((conv) => (conv.id === id ? { ...conv, name: updatedConversation.name } : conv))
      );
    } catch (error) {
      console.error("Error updating conversation:", error);
    }
  };

  const handleDeleteConversation = async (id) => {
    try {
      await deleteConversation(id);
      setConversations((prev) => prev.filter((conv) => conv.id !== id));
      if (selectedConversation === id) {
        setSelectedConversation(null);
        setMessages([]);
      }
    } catch (error) {
      console.error("Error deleting conversation:", error);
    }
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <ConversationList
        conversations={conversations}
        onSelectConversation={handleSelectConversation}
        onEditConversation={handleEditConversation}
        onDeleteConversation={handleDeleteConversation}
      />
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <ChatWindow messages={messages} />
        <MessageInput onSendMessage={handleSendMessage} />
      </Box>
      <Button
        variant="contained"
        color="primary"
        onClick={handleOpenDialog}
        sx={{ position: 'absolute', top: 16, right: 16 }}
      >
        Nueva Conversación
      </Button>
      <Dialog open={dialogOpen} onClose={handleCloseDialog}>
        <DialogTitle>Nueva Conversación</DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            variant="outlined"
            label="Título"
            value={newConversationTitle}
            onChange={(e) => setNewConversationTitle(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancelar</Button>
          <Button onClick={handleAddConversation} color="primary" variant="contained">
            Crear
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ChatPage;
