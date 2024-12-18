import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#2E7D32', // Un verde oscuro para representar estabilidad financiera.
    },
    secondary: {
      main: '#01579B', // Un azul oscuro, que transmite confianza y seriedad.
    },
    background: {
      default: '#121212', // Fondo oscuro para mejorar la lectura.
      paper: '#1E1E1E', // Un tono ligeramente más claro para los elementos de la interfaz.
    },
    text: {
      primary: '#E0E0E0', // Texto claro sobre fondo oscuro.
      secondary: '#B0BEC5', // Texto secundario, más suave.
    },
    action: {
      active: '#81C784', // Un verde suave para los elementos activos.
      hover: '#388E3C', // Un verde más oscuro para el hover.
      selected: '#2C6B32', // Un verde oscuro para los elementos seleccionados.
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
