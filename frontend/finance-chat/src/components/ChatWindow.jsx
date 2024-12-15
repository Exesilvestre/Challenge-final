import React, { useEffect, useRef } from 'react';
import { Box } from '@mui/material';
import MessageItem from './MessageItem';

const ChatWindow = ({ messages }) => {
  const chatEndRef = useRef(null);  // Referencia al final del chat

  useEffect(() => {
    // Desplazar hacia el final cada vez que los mensajes cambian
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  return (
    <Box
      sx={{
        flex: 1,
        padding: 2,
        overflowY: 'auto',
        backgroundColor: 'background.default',
        borderRadius: 2,
        height: '400px',
        margin: '5rem',
      }}
    >
      {messages.map((message, index) => (
        <MessageItem
          key={index}
          message={message}
          isUser={message.role === 'user'} // Cambiado a 'role' en vez de 'sender'
        />
      ))}
      
      {/* Elemento invisible que se usa para desplazar el chat al final */}
      <div ref={chatEndRef} />
    </Box>
  );
};

export default ChatWindow;
