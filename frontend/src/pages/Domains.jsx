import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { getDomains } from '../api';
import AddDomainForm from '../components/AddDomainForm';
import DomainDetails from '../components/DomainDetails';
import ConfirmDialog from '../components/ConfirmDialog';
import { FaTrash } from 'react-icons/fa';
import './Domains.css';

const Domains = () => {
    const [domains, setDomains] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedDomain, setSelectedDomain] = useState(null);

    useEffect(() => {
        const fetchDomains = async () => {
            try {
                const data = await getDomains();
                setDomains(data);
            } catch (err) {
                toast.error(err.response?.data?.detail || err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchDomains();
    }, []);

    const handleDomainAdded = (newDomain) => {
        setDomains((prevDomains) => [...prevDomains, newDomain]);
    };

    const handleDeleteDomain = async (domainName) => {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/domain/${domainName}`);
            setDomains((prevDomains) => prevDomains.filter(domain => domain.name !== domainName));
            if (selectedDomain && selectedDomain.name === domainName) {
                setSelectedDomain(null);
            }
            toast.success(`Domain ${domainName} deleted successfully`);
        } catch (err) {
            toast.error(err.response?.data?.detail || err.message);
        }
    };

    const confirmDeleteDomain = (domainName, event) => {
        event.stopPropagation(); // Prevent selecting the domain when clicking the delete button
        ConfirmDialog({
            title: 'Confirm Deletion',
            message: `Are you sure you want to delete the domain "${domainName}"?`,
            onConfirm: () => handleDeleteDomain(domainName),
            onCancel: () => {}
        });
    };

    const filteredDomains = domains.filter(domain =>
        domain.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="domains-container">
            <h1>Domains List</h1>
            <div className="top-controls">
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search domains..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="add-domain-form">
                    <AddDomainForm onDomainAdded={handleDomainAdded} />
                </div>
            </div>
            <div className="domains-list-container">
                {filteredDomains.length === 0 ? (
                    <div>No domains available</div>
                ) : (
                    <ul className="domains-list">
                        {filteredDomains.map((domain) => (
                            <li key={domain.id} onClick={() => setSelectedDomain(domain)} className="domain-item">
                                <span>{domain.name}</span>
                                <button
                                    className="delete-button"
                                    onClick={(e) => confirmDeleteDomain(domain.name, e)}
                                >
                                    <FaTrash color="red" size={16} />
                                </button>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            {selectedDomain && (
                <DomainDetails domain={selectedDomain} />
            )}
        </div>
    );
};

export default Domains;
