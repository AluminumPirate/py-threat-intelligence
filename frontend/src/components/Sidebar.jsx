import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
    Drawer,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
    Toolbar,
    Typography,
    IconButton,
    Box,
} from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import DomainIcon from '@mui/icons-material/Domain';
import ScanIcon from '@mui/icons-material/FindInPage';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { useTheme } from '@mui/material/styles';

const drawerWidth = 240;

const Sidebar = ({ open, setOpen, toggleTheme }) => {
    const theme = useTheme();
    const location = useLocation();

    const handleDrawerToggle = () => {
        setOpen(!open);
    };

    const drawer = (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Toolbar>
                <Typography variant="h6" noWrap>
                    Navigation
                </Typography>
                <IconButton onClick={handleDrawerToggle} style={{ marginLeft: 'auto' }}>
                    {open ? <ChevronLeftIcon /> : <ChevronRightIcon />}
                </IconButton>
            </Toolbar>
            <List style={{ flexGrow: 1 }}>
                <ListItem
                    button
                    component={Link}
                    to="/home"
                    selected={location.pathname === '/home'}
                >
                    <ListItemIcon>
                        <HomeIcon />
                    </ListItemIcon>
                    <ListItemText primary="Home" />
                </ListItem>
                <ListItem
                    button
                    component={Link}
                    to="/domains"
                    selected={location.pathname === '/domains'}
                >
                    <ListItemIcon>
                        <DomainIcon />
                    </ListItemIcon>
                    <ListItemText primary="Domains" />
                </ListItem>
                <ListItem
                    button
                    component={Link}
                    to="/scans"
                    selected={location.pathname === '/scans'}
                >
                    <ListItemIcon>
                        <ScanIcon />
                    </ListItemIcon>
                    <ListItemText primary="Scans" />
                </ListItem>
            </List>
            <Box sx={{ textAlign: 'center', pb: 2 }}>
                <IconButton onClick={toggleTheme} color="inherit">
                    {theme.palette.mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
                </IconButton>
            </Box>
        </div>
    );

    return (
        <>
            <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ display: { sm: 'none' } }}
            >
                <MenuIcon />
            </IconButton>
            <Drawer
                variant="permanent"
                sx={{
                    display: { xs: 'none', sm: 'block' },
                    '& .MuiDrawer-paper': {
                        boxSizing: 'border-box',
                        width: open ? drawerWidth : theme.spacing(7),
                        backgroundColor: theme.palette.sidebar.main,
                        color: theme.palette.sidebar.contrastText,
                    },
                }}
                open={open}
            >
                {drawer}
            </Drawer>
            <Drawer
                variant="temporary"
                open={open}
                onClose={handleDrawerToggle}
                ModalProps={{
                    keepMounted: true,
                }}
                sx={{
                    display: { xs: 'block', sm: 'none' },
                    '& .MuiDrawer-paper': {
                        boxSizing: 'border-box',
                        width: drawerWidth,
                        backgroundColor: theme.palette.sidebar.main,
                        color: theme.palette.sidebar.contrastText,
                    },
                }}
            >
                {drawer}
            </Drawer>
        </>
    );
};

export default Sidebar;
