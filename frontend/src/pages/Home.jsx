import React from 'react';
import { Container, Typography, Grid, Card, CardContent, CardActionArea, CardMedia } from '@mui/material';
import { Link } from 'react-router-dom';
import domainsImage from '../assets/domains.svg';
import scansImage from '../assets/scans.svg';
import './Home.css';

const Home = () => {
    return (
        <Container className="home-container">
            <Typography variant="h2" component="h1" gutterBottom>
                Welcome to the Threat Intelligence System
            </Typography>
            <Typography variant="h5" component="h2" gutterBottom>
                Manage domains and perform scans to check security against multiple sources.
            </Typography>
            <Grid container spacing={3} className="home-grid">
                <Grid item xs={12} sm={6}>
                    <Card className="home-card">
                        <CardActionArea component={Link} to="/domains">
                            <CardMedia
                                component="img"
                                alt="Manage Domains"
                                image={domainsImage}
                                title="Manage Domains"
                            />
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Manage Domains
                                </Typography>
                                <Typography variant="body2" color="textSecondary" component="p">
                                    Add, delete, view domains in the system and view scan results.
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <Card className="home-card">
                        <CardActionArea component={Link} to="/scans">
                            <CardMedia
                                component="img"
                                alt="Perform Scans"
                                image={scansImage}
                                title="Perform Scans"
                            />
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Perform Scans
                                </Typography>
                                <Typography variant="body2" color="textSecondary" component="p">
                                    Run security scans on domains.
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Home;
