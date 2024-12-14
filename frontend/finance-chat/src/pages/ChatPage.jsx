import React, { useState, useEffect } from 'react';
import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';
import { v4 as uuidv4 } from 'uuid';
import ChatWindow from '../components/ChatWindow';
import ConversationList from '../components/ConversationList';
import MessageInput from '../components/MessageInput';
import { fetchMessages, sendMessage } from '../services/api';

const ChatPage = () => {
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newConversationTitle, setNewConversationTitle] = useState('');

  useEffect(() => {
    // Simulate fetching conversations from an API
    const loadConversations = async () => {
      setConversations([
        { id: uuidv4(), title: 'Conversación 1' },
        { id: uuidv4(), title: 'Conversación 2' },
      ]);
    };
    loadConversations();
  }, []);

  const handleSelectConversation = async (conversationId) => {
    setSelectedConversation(conversationId);
    const data = await fetchMessages(conversationId);
    setMessages(data);
  };

  const handleSendMessage = async (text) => {
    if (selectedConversation) {
      const newMessage = await sendMessage(selectedConversation, text);
      setMessages((prev) => [...prev, newMessage]);
    }
  };

  const handleOpenDialog = () => setDialogOpen(true);
  const handleCloseDialog = () => {
    setDialogOpen(false);
    setNewConversationTitle('');
  };

  const handleAddConversation = () => {
    if (newConversationTitle.trim()) {
      const newConversation = { id: uuidv4(), title: newConversationTitle };
      setConversations((prev) => [...prev, newConversation]);
      handleCloseDialog();
    }
  };

  const handleEditConversation = (id, newTitle) => {
    setConversations((prev) =>
      prev.map((conv) => (conv.id === id ? { ...conv, title: newTitle } : conv))
    );
  };

  const handleDeleteConversation = (id) => {
    setConversations((prev) => prev.filter((conv) => conv.id !== id));
    if (selectedConversation === id) {
      setSelectedConversation(null);
      setMessages([]);
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