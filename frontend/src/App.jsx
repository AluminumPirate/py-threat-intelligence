import React, {Suspense, useEffect, useState} from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import CustomToastContainer from './ToastContainer.jsx';
import Sidebar from './components/Sidebar';
import {lightTheme, darkTheme} from './theme';

import './App.css';
import './index.css';
import {CssBaseline, ThemeProvider} from "@mui/material";


const Home = React.lazy(() => import('./pages/Home'));
const Domains = React.lazy(() => import('./pages/Domains'));
const Scans = React.lazy(() => import('./pages/Scans'));
const NotFound = React.lazy(() => import('./pages/NotFound'));

const App = () => {
    // Initialize theme from localStorage or default to lightTheme
    const savedTheme = localStorage.getItem('theme');
    const initialTheme = savedTheme === 'dark' ? darkTheme : lightTheme;
    const [theme, setTheme] = useState(initialTheme);
    const [open, setOpen] = useState(true);

    // Save theme to localStorage whenever it changes
    useEffect(() => {
        const themeMode = theme === lightTheme ? 'light' : 'dark';
        console.log(`Saving theme to localStorage: ${themeMode}`);
        localStorage.setItem('theme', themeMode);
    }, [theme]);

    const toggleTheme = () => {
        setTheme((prevTheme) => (prevTheme === lightTheme ? darkTheme : lightTheme));
    };
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <div style={{ display: 'flex' }}>
                    <Sidebar open={open} setOpen={setOpen} toggleTheme={toggleTheme} />
                    <div
                        style={{
                            flexGrow: 1,
                            padding: '20px',
                            transition: 'margin 0.3s',
                            marginLeft: open ? '240px' : theme.spacing(7),
                        }}
                    >
                        <Suspense fallback={<div>Loading...</div>}>
                            <Routes>
                                <Route path="/" element={<Navigate to="/home" />} />
                                <Route path="/home" element={<Home />} />
                                <Route path="/domains" element={<Domains />} />
                                <Route path="/scans" element={<Scans />} />
                                <Route path="*" element={<NotFound />} />
                            </Routes>
                        </Suspense>
                    </div>
                    <CustomToastContainer />
                </div>
            </Router>
        </ThemeProvider>
    );
};


export default App;
