import React, { useState } from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  Menu,
  MenuItem,
} from '@mui/material';
import MoreVertIcon from '@mui/icons-material/MoreVert';

const ConversationList = ({ conversations, onSelectConversation, onEditConversation, onDeleteConversation }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedId, setSelectedId] = useState(null);

  const handleOpenMenu = (event, id) => {
    setAnchorEl(event.currentTarget);
    setSelectedId(id);
  };

  const handleCloseMenu = () => {
    setAnchorEl(null);
    setSelectedId(null);
  };

  const handleEdit = () => {
    const newTitle = prompt('Nuevo título:', conversations.find((c) => c.id === selectedId)?.title);
    if (newTitle) onEditConversation(selectedId, newTitle);
    handleCloseMenu();
  };

  const handleDelete = () => {
    if (window.confirm('¿Eliminar conversación?')) onDeleteConversation(selectedId);
    handleCloseMenu();
  };

  return (
    <Box
      sx={{
        width: 250,
        height: '100%',
        backgroundColor: '#333',
        padding: 2,
        border: '1px solid #fff',
        borderRadius: 8,
        overflowY: 'auto',
      }}
    >
      <Typography variant="h6" gutterBottom color="primary">
        Conversaciones
      </Typography>
      <List>
        {conversations.map((conversation) => (
          <ListItem
            button
            key={conversation.id}
            sx={{
              '&:hover': {
                backgroundColor: 'primary.main',
                color: 'background.default',
              },
            }}
            onClick={() => onSelectConversation(conversation.id)}
          >
            <ListItemText primary={conversation.title} />
            <IconButton
              size="small"
              sx={{ color: 'text.secondary' }}
              onClick={(e) => handleOpenMenu(e, conversation.id)}
            >
              <MoreVertIcon />
            </IconButton>
          </ListItem>
        ))}
      </List>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleCloseMenu}
        PaperProps={{
          style: { backgroundColor: '#444', color: '#fff' },
        }}
      >
        <MenuItem onClick={handleEdit}>Editar</MenuItem>
        <MenuItem onClick={handleDelete}>Eliminar</MenuItem>
      </Menu>
    </Box>
  );
};

export default ConversationList;
