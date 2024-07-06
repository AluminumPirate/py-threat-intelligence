import React, { useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import './AddDomainForm.css';

const AddDomainForm = ({ onDomainAdded }) => {
    const [domainName, setDomainName] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const response = await axios.post(`${import.meta.env.VITE_API_URL}/domain`, {
                name: domainName,
            });
            setDomainName('');
            onDomainAdded(response.data);
            toast.success(`Domain ${domainName} added successfully`);
        } catch (err) {
            if (err.response && err.response.data && err.response.data.detail) {
                toast.error(err.response.data.detail);
            } else {
                toast.error(err.message);
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="inline-form">
            <input
                type="text"
                value={domainName}
                onChange={(e) => setDomainName(e.target.value)}
                placeholder="Enter domain name"
                required
            />
            <button type="submit" disabled={loading}>
                {loading ? 'Adding...' : 'Add Domain'}
            </button>
        </form>
    );
};

export default AddDomainForm;
