import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2196F3',
    },
    secondary: {
      main: '#607D8B',
    },
    background: {
      default: '#121212',
      paper: '#1E1E1E',
    },
    text: {
      primary: '#E0E0E0',
      secondary: '#B0BEC5',
    },
    action: {
      active: '#64B5F6',
      hover: '#1976D2',
      selected: '#1565C0',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h6: {
      fontWeight: '500',
    },
    body1: {
      lineHeight: 1.5,
    },
  },
});

export default theme;
