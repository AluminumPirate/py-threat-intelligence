import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { Collapse } from 'react-collapse';
import ConfirmDialog from '../components/ConfirmDialog';
import { FaTrash } from 'react-icons/fa';
import './DomainDetails.css';

const DomainDetails = ({ domain }) => {
    const [latestScan, setLatestScan] = useState(null);
    const [allScans, setAllScans] = useState([]);
    const [loading, setLoading] = useState(false);
    const [showAllScans, setShowAllScans] = useState(false);
    const [sortOrder, setSortOrder] = useState('desc');
    const [openScanId, setOpenScanId] = useState(null);

    useEffect(() => {
        const fetchDomainDetails = async () => {
            try {
                const response = await axios.get(`${import.meta.env.VITE_API_URL}/domain/${domain.name}`);
                const domainData = response.data;
                setLatestScan(domainData.last_scan || null);
                setShowAllScans(false);
                setAllScans([]);
                setOpenScanId(null);
            } catch (err) {
                toast.error(err.response?.data?.detail || err.message);
            }
        };

        fetchDomainDetails();
    }, [domain]);

    const handleLoadMoreScans = async () => {
        setLoading(true);
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/domain/${domain.name}/all-scans`);
            if (response.data.scans && Array.isArray(response.data.scans)) {
                const filteredScans = response.data.scans.filter(scan =>
                    scan.status === 'completed' || scan.status === 'partially succeeded'
                );
                setAllScans(filteredScans);
                setShowAllScans(true);
            } else {
                throw new Error('Invalid data format');
            }
        } catch (err) {
            toast.error(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSortScans = () => {
        const sortedScans = [...allScans].sort((a, b) => {
            return sortOrder === 'asc'
                ? new Date(a.created_at) - new Date(b.created_at)
                : new Date(b.created_at) - new Date(a.created_at);
        });
        setAllScans(sortedScans);
        setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    };

    const toggleScan = (scanId) => {
        setOpenScanId(openScanId === scanId ? null : scanId);
    };

    const handleDeleteScan = async (scanId) => {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/domain/scan/${scanId}`);
            setAllScans((prevScans) => prevScans.filter(scan => scan.id !== scanId));
            if (latestScan && latestScan.id === scanId) {
                setLatestScan(null);
            }
            toast.success(`Scan ${scanId} deleted successfully`);
        } catch (err) {
            toast.error(err.response?.data?.detail || err.message);
        }
    };

    const confirmDeleteScan = (scanId, event) => {
        event.stopPropagation(); // Prevent toggling the accordion when clicking the delete button
        ConfirmDialog({
            title: 'Confirm Deletion',
            message: `Are you sure you want to delete the scan "${scanId}"?`,
            onConfirm: () => handleDeleteScan(scanId),
            onCancel: () => {}
        });
    };

    return (
        <div className="domain-details">
            <h2>Domain Details</h2>
            <div className="domain-header">
                <p><strong>Name:</strong> {domain.name}</p>
            </div>
            <p><strong>Latest Scan:</strong> {latestScan ? new Date(latestScan.created_at).toLocaleString() : 'Not scanned yet'}</p>
            <p><strong>Last Scan Data:</strong></p>
            {latestScan ? <pre>{JSON.stringify(latestScan.data, null, 2)}</pre> : <p>No scan data available.</p>}

            {showAllScans && (
                <>
                    <h3>All Scans</h3>
                    <button onClick={handleSortScans}>Sort by Creation Time ({sortOrder === 'asc' ? 'Ascending' : 'Descending'})</button>
                    <ul className="scans-list">
                        {allScans.map((scan) => (
                            <li key={scan.id}>
                                <div onClick={() => toggleScan(scan.id)} className="scan-header">
                                    <div>
                                        <p><strong>Scan ID:</strong> {scan.id}</p>
                                        <p><strong>Status:</strong> {scan.status}</p>
                                        <p><strong>Created At:</strong> {new Date(scan.created_at).toLocaleString()}</p>
                                    </div>
                                    <button
                                        className="delete-button"
                                        onClick={(e) => confirmDeleteScan(scan.id, e)}
                                    >
                                        <FaTrash color="red" size={14} />
                                    </button>
                                </div>
                                <Collapse isOpened={openScanId === scan.id}>
                                    <div className="scan-content">
                                        <pre>{JSON.stringify(scan.data, null, 2)}</pre>
                                    </div>
                                </Collapse>
                            </li>
                        ))}
                    </ul>
                </>
            )}

            {!showAllScans && (
                <button onClick={handleLoadMoreScans} disabled={loading}>
                    {loading ? 'Loading...' : 'Load More Scans'}
                </button>
            )}
        </div>
    );
};

export default DomainDetails;
