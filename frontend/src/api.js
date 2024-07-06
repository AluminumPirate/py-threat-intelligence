import axios from 'axios';

// Set the base URL for the API using Vite environment variables
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3004';

// Create an instance of axios
const api = axios.create({
    baseURL: API_URL,
});

export const getDomains = async () => {
    try {
        const response = await api.get('/domains');
        console.log('API Response:', response.data);  // Debugging line
        return response.data;
    } catch (error) {
        console.error('Error fetching domains:', error);
        throw error;
    }
};
