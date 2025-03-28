import { useState, useEffect } from "react";
import BudgetItem from "../../types/BudgetItem";

const EditBudgetModal = ({
    budget,
    onSave,
    onCancel,
}: {
    budget: BudgetItem;
    onSave: (budget: BudgetItem) => void;
    onCancel: () => void;
}) => {
    const [editedBudget, setEditedBudget] = useState(() => {
        const amount = parseFloat(budget.amount);
        const spent = parseFloat(budget.spent);
        return {
            ...budget,
            amount: isNaN(amount) || amount < 0 ? '0' : String(amount),
            spent: isNaN(spent) || spent < 0 ? '0' : String(spent)
        };
    });

    useEffect(() => {
        const handleEscape = (e: KeyboardEvent) => {
            if (e.key === 'Escape') {
                onCancel();
            }
        };

        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, [onCancel]);

    useEffect(() => {
        const amount = parseFloat(budget.amount);
        const spent = parseFloat(budget.spent);
        setEditedBudget({
            ...budget,
            amount: isNaN(amount) || amount < 0 ? '0' : String(amount),
            spent: isNaN(spent) || spent < 0 ? '0' : String(spent)
        });
    }, [budget, onCancel]);

    const handleOverlayClick = (e: React.MouseEvent) => {
        if (e.target === e.currentTarget) {
            onCancel();
        }
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (editedBudget.category.trim()) {
            try {
                onSave(editedBudget);
            } catch (error) {
                // Handle error silently
                console.error('Failed to save budget:', error);
            }
        }
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value, type } = e.target;
        let newValue = value;

        if (type === 'number') {
            const numValue = parseFloat(value);
            if (isNaN(numValue) || numValue < 0) {
                newValue = '0';
            }
        } else {
            // Remove special characters from text inputs
            newValue = value.replace(/[^a-zA-Z0-9\s]/g, '');
        }

        setEditedBudget(prev => ({ ...prev, [name]: newValue }));
    };

    return (
        <div 
            data-testid="modal-overlay"
            className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
            onClick={handleOverlayClick}>
            <div 
                role="dialog"
                aria-labelledby="modal-title"
                className="bg-white p-6 rounded-md shadow-md w-full max-w-md"
                key={`${budget.category}-${budget.amount}-${budget.spent}-${budget.frequency}`}>
                <h2 id="modal-title" className="text-2xl font-bold mb-4">Edit Budget</h2>
                <form className="flex flex-col gap-4" onSubmit={handleSubmit} key={`${budget.category}-${budget.amount}-${budget.spent}-${budget.frequency}`}>
                    <div>
                        <label htmlFor="category">Category:</label>
                        <input
                            id="category"
                            type="text"
                            name="category"
                            value={editedBudget.category}
                            onChange={handleInputChange}
                            className="border border-gray-300 p-2 rounded-md w-full"
                            tabIndex={0}
                        />
                    </div>
                    <div>
                        <label htmlFor="amount">Total Amount:</label>
                        <input
                            id="amount"
                            type="number"
                            name="amount"
                            value={editedBudget.amount}
                            onChange={handleInputChange}
                            className="border border-gray-300 p-2 rounded-md w-full"
                            tabIndex={1}
                        />
                    </div>
                    <div>
                        <label htmlFor="spent">Spent:</label>
                        <input
                            id="spent"
                            type="number"
                            name="spent"
                            value={editedBudget.spent}
                            onChange={handleInputChange}
                            className="border border-gray-300 p-2 rounded-md w-full"
                            tabIndex={2}
                        />
                    </div>
                    <div>
                        <label htmlFor="frequency">Frequency:</label>
                        <input
                            id="frequency"
                            type="text"
                            name="frequency"
                            value={editedBudget.frequency}
                            onChange={handleInputChange}
                            className="border border-gray-300 p-2 rounded-md w-full"
                            tabIndex={3}
                        />
                    </div>
                    <div className="flex justify-end gap-2">
                        <button
                            type="submit"
                            className="bg-green-400 text-white px-4 py-2 rounded-md"
                            tabIndex={4}
                        >
                            Save
                        </button>
                        <button
                            type="button"
                            className="bg-gray-500 text-white px-4 py-2 rounded-md"
                            onClick={onCancel}
                            tabIndex={5}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EditBudgetModal