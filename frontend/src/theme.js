import { createTheme } from '@mui/material/styles';

// Light theme
const lightTheme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#1976d2', // Update this to your primary color
        },
        secondary: {
            main: '#dc004e', // Update this to your secondary color
        },
        background: {
            default: '#f4f6f8',
            paper: '#ffffff',
        },
        sidebar: {
            main: '#1976d2',
            contrastText: '#fff',
        },
        text: {
            primary: '#000', // Adjust text color
            secondary: '#333', // Adjust secondary text color
        },
    },
    typography: {
        h1: {
            fontSize: '2rem',
            fontWeight: 'bold',
        },
        h2: {
            fontSize: '1.5rem',
            fontWeight: 'bold',
        },
        body1: {
            fontSize: '1rem',
        },
    },
    components: {
        MuiDrawer: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#1976d2',
                    color: '#fff',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none', // Prevent all caps
                },
            },
        },
    },
});

// Dark theme
const darkTheme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#90caf9', // Update this to your primary color
        },
        secondary: {
            main: '#f48fb1', // Update this to your secondary color
        },
        background: {
            default: '#121212',
            paper: '#1e1e1e',
        },
        sidebar: {
            main: '#333',
            contrastText: '#fff',
        },
        text: {
            primary: '#fff', // Adjust text color
            secondary: '#aaa', // Adjust secondary text color
        },
    },
    typography: {
        h1: {
            fontSize: '2rem',
            fontWeight: 'bold',
        },
        h2: {
            fontSize: '1.5rem',
            fontWeight: 'bold',
        },
        body1: {
            fontSize: '1rem',
        },
    },
    components: {
        MuiDrawer: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#333',
                    color: '#fff',
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    textTransform: 'none', // Prevent all caps
                },
            },
        },
    },
});

export { lightTheme, darkTheme };
