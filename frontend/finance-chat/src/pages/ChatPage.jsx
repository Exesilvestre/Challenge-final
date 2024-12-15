import React, { useState, useEffect } from 'react';
import { Box, Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, CircularProgress } from '@mui/material';
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
  const [loading, setLoading] = useState(false); // Estado de carga

  useEffect(() => {
    // Cargar las conversaciones cuando se monta el componente
    const loadConversations = async () => {
      try {
        const data = await fetchConversations();
        setConversations(data);
        
        // Seleccionar la primera conversación si está disponible
        if (data.length > 0) {
          const firstConversationId = data[0].id;
          setSelectedConversation(firstConversationId);

          // Fetch de los mensajes de la primera conversación
          const messagesData = await fetchMessages(firstConversationId);
          setMessages(messagesData);
        }
      } catch (error) {
        console.error("Error fetching conversations:", error);
      }
    };
    loadConversations();
  }, []);

  const handleSelectConversation = async (conversationId) => {
    setSelectedConversation(conversationId);
    try {
      const data = await fetchMessages(conversationId);
      setMessages(data);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const handleSendMessage = async (text) => {

    if (selectedConversation) {
      const newMessage = { content: text, role: 'user' };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      try {
        setLoading(true)
        const response = await sendMessage(selectedConversation, text);
        const repsonseMessage = {content: response.response, role: 'assistant'}
        setMessages((prevMessages) => [...prevMessages, repsonseMessage]);
        setLoading(false)
      } catch (error) {
        setMessages((prevMessages) => prevMessages.filter(msg => msg !== newMessage));
        alert('Error sending message');
        setLoading(false)
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
      const updatedConversation = await updateConversation(id, newTitle);
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
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: 2 }}>
            <CircularProgress />
          </Box>
        )}
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
