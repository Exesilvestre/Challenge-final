import React from 'react';
import { Box, Typography } from '@mui/material';

const ChatWindow = ({ messages }) => {
  return (
    <Box
        sx={{
            flex: 1,
            padding: 2,
            overflowY: 'auto',
            backgroundColor: 'background.default',
            borderRadius: 2,
        }}
        >
        {messages.map((message, index) => (
            <Box
            key={index}
            sx={{
                marginBottom: 2,
                textAlign: message.sender === 'user' ? 'right' : 'left',
            }}
            >
            <Typography
                variant="body1"
                sx={{
                padding: 1,
                backgroundColor: message.sender === 'user' ? 'primary.main' : 'secondary.main',
                color: message.sender === 'user' ? 'background.default' : 'text.primary',
                borderRadius: 2,
                display: 'inline-block',
                }}
            >
                {message.text}
            </Typography>
            </Box>
        ))}
    </Box>
  );
};

export default ChatWindow;
