import React from 'react';
import { Box, Typography } from '@mui/material';

const MessageItem = ({ message, isUser }) => {
    return (
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          marginBottom: 2,
        }}
      >
        <Box
          sx={{
            maxWidth: '70%',
            backgroundColor: isUser ? 'primary.main' : 'grey.800', // Fondo más oscuro para assistant
            color: isUser ? 'background.default' : 'text.primary',
            padding: 1.5,
            borderRadius: 2,
          }}
        >
          <Typography variant="body1">{message.content}</Typography>
        </Box>
      </Box>
    );
  };
  

export default MessageItem;
