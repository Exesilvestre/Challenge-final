import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';

const MessageInput = ({ onSendMessage }) => {
  const [message, setMessage] = useState('');

  const handleSendMessage = () => {
    if (message.trim()) {
      onSendMessage(message);
      setMessage('');  // Clear input after sending the message
    }
  };

  return (
    <Box sx={{ display: 'flex', padding: 2, backgroundColor: 'background.paper', border: '1px solid #fff', borderRadius: 8, marginLeft:'1.5rem', marginRight: '1.5rem' }}>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="Escribe tu mensaje..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        sx={{
          '& .MuiOutlinedInput-root': {
            backgroundColor: 'background.default',
            color: 'text.primary',
            '&:hover fieldset': {
              borderColor: 'primary.main',
            },
            '&.Mui-focused fieldset': {
              borderColor: 'primary.main',
            },
          },
        }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleSendMessage}
        sx={{ marginLeft: 2 }}
      >
        Enviar
      </Button>
    </Box>
  );
};

export default MessageInput;
