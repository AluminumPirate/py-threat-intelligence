import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { FaCheck, FaSpinner } from 'react-icons/fa';
import ConfirmDialog from '../components/ConfirmDialog.jsx';
import './Scans.css';
import './Domains.css';

const Scans = () => {
    const [domains, setDomains] = useState([]);
    const [selectedDomains, setSelectedDomains] = useState([]);
    const [loading, setLoading] = useState(false);
    const [scanStatus, setScanStatus] = useState({});
    const [disableCheckboxes, setDisableCheckboxes] = useState(false);

    useEffect(() => {
        const fetchDomains = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/domains`);
                setDomains(response.data);
            } catch (err) {
                toast.error(err.response?.data?.detail || err.message);
            }
        };

        fetchDomains();
    }, []);

    const toggleDomainSelection = (domainName) => {
        setSelectedDomains((prevSelected) =>
            prevSelected.includes(domainName)
                ? prevSelected.filter((name) => name !== domainName)
                : [...prevSelected, domainName]
        );
    };

    const runScan = async (domainName) => {
        try {
            setScanStatus((prevStatus) => ({ ...prevStatus, [domainName]: 'loading' }));
            await axios.post(`${import.meta.env.VITE_API_URL}/domain/${domainName}/scan`);
            setScanStatus((prevStatus) => ({ ...prevStatus, [domainName]: 'completed' }));
        } catch (err) {
            setScanStatus((prevStatus) => ({ ...prevStatus, [domainName]: 'failed' }));
            toast.error(err.response?.data?.detail || err.message);
        }
    };

    const runScansForSelectedDomains = async () => {
        if (selectedDomains.length > 1) {
            ConfirmDialog({
                title: 'Confirm Bulk Scan',
                message: 'Are you sure you want to scan the selected domains?',
                onConfirm: async () => {
                    setLoading(true);
                    const scanPromises = selectedDomains.map((domainName) => runScan(domainName));
                    await Promise.all(scanPromises);
                    setSelectedDomains([]); // Uncheck all checkboxes after scanning
                    setLoading(false);
                },
                onCancel: () => {},
            });
        } else {
            setLoading(true);
            await runScan(selectedDomains[0]);
            setSelectedDomains([]); // Uncheck the checkbox after scanning
            setLoading(false);
        }
    };

    const runScanJobForAllDomains = async () => {
        ConfirmDialog({
            title: 'Confirm Scan Job for All Domains',
            message: 'Are you sure you want to run a scan job for all domains?',
            onConfirm: async () => {
                setLoading(true);
                setDisableCheckboxes(true); // Disable all checkboxes
                try {
                    await axios.post(`${import.meta.env.VITE_API_URL}/jobs`);
                    toast.success('Scan job initiated for all domains');
                } catch (err) {
                    toast.error(err.response?.data?.detail || err.message);
                } finally {
                    setLoading(false);
                    setDisableCheckboxes(false); // Enable checkboxes after job is complete
                }
            },
            onCancel: () => {},
        });
    };

    return (
        <div className="scans-container">
            <h1>Scans Page</h1>
            <div className="domains-list-container">
                <h2>Domains List</h2>
                <ul className="domains-list">
                    {domains.map((domain) => (
                        <li key={domain.name} className="domain-item">
                            <span>{domain.name}</span>
                            {scanStatus[domain.name] === 'loading' && <FaSpinner className="loading-icon" />}
                            {scanStatus[domain.name] === 'completed' && <FaCheck className="completed-icon" />}
                            <input
                                type="checkbox"
                                checked={selectedDomains.includes(domain.name)}
                                onChange={() => toggleDomainSelection(domain.name)}
                                className="checkbox"
                                disabled={disableCheckboxes}
                            />
                        </li>
                    ))}
                </ul>
            </div>
            <div className="buttons-container">
                <button onClick={runScansForSelectedDomains} disabled={loading || selectedDomains.length === 0}>
                    {loading ? 'Scanning...' : 'Run Scans for Selected Domains'}
                </button>
                <button className="run-all-button" onClick={runScanJobForAllDomains} disabled={loading}>
                    {loading ? 'Running Job...' : 'Run Scan Job for All Domains'}
                </button>
            </div>
        </div>
    );
};

export default Scans;
