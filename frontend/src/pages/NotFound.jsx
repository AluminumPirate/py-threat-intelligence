import React from 'react';
import { Link } from 'react-router-dom';
import { Button, Container, Typography } from '@mui/material';
import './NotFound.css';
import notFoundImage from '../assets/not-found.svg';


const NotFound = () => {
    return (
        <Container className="not-found-container">
            <Typography variant="h2" component="h1" gutterBottom>
                Oops! Page not found.
            </Typography>
            <img
                src={notFoundImage} // Replace with a whimsical image URL
                alt="Page not found"
                className="not-found-image"
            />
            <Typography variant="h5" component="h2" gutterBottom>
                The page you're looking for doesn't exist.
            </Typography>
            <Button variant="contained" color="primary" component={Link} to="/home">
                Go to Home
            </Button>
        </Container>
    );
};

export default NotFound;
