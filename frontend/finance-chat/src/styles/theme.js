import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2ECC71', // Verde financiero
    },
    secondary: {
      main: '#BFC9CA', // Plata
    },
    background: {
      default: '#1B263B', // Azul oscuro
      paper: '#343A40', // Gris carbón
    },
    text: {
      primary: '#E5E8E8', // Blanco suave
      secondary: '#BFC9CA', // Plata
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
    h6: {
      fontWeight: 'bold',
    },
    body1: {
      lineHeight: 1.6,
    },
  },
});

export default theme;
