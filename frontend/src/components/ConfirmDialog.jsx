import React from 'react';
import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';
import './confirmDialog.css'; // Import custom CSS

const ConfirmDialog = ({ title, message, onConfirm, onCancel }) => {
    confirmAlert({
        customUI: ({ onClose }) => {
            return (
                <div className='custom-ui'>
                    <h1>{title}</h1>
                    <p>{message}</p>
                    <button onClick={() => {
                        onConfirm();
                        onClose();
                    }}>Yes</button>
                    <button onClick={() => {
                        onCancel();
                        onClose();
                    }}>No</button>
                </div>
            );
        }
    });
};

export default ConfirmDialog;
