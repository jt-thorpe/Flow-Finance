import { useState } from "react";
import BudgetItem from "../../app/types/BudgetItem";


const EditBudgetModal = ({
    budget,
    onSave,
    onCancel,
}: {
    budget: BudgetItem;
    onSave: (budget: BudgetItem) => void;
    onCancel: () => void;
}) => {
    const [editedBudget, setEditedBudget] = useState({ ...budget });
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
            onClick={(e) => e.stopPropagation()}>
            <div className="bg-white p-6 rounded-md shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-4">Edit Budget</h2>
                <form className="flex flex-col gap-4">
                    <label>
                        Category:
                        <input
                            type="text"
                            name="category"
                            value={editedBudget.category}
                            onChange={(e) =>
                                setEditedBudget({ ...editedBudget, category: e.target.value })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Total Amount:
                        <input
                            type="number"
                            name="amount"
                            value={editedBudget.amount}
                            onChange={(e) =>
                                setEditedBudget({ ...editedBudget, amount: parseFloat(e.target.value) })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Spent:
                        <input
                            type="number"
                            name="spent"
                            value={editedBudget.spent}
                            onChange={(e) =>
                                setEditedBudget({ ...editedBudget, spent: parseFloat(e.target.value) })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Frequency:
                        <input
                            type="text"
                            name="frequency"
                            value={editedBudget.frequency}
                            onChange={(e) =>
                                setEditedBudget({ ...editedBudget, frequency: e.target.value })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <div className="flex justify-end gap-2">
                        <button
                            type="button"
                            className="bg-green-400 text-white px-4 py-2 rounded-md"
                            onClick={() => {
                                // TODO: Add your save logic here (e.g., API call)
                                console.log("Updated Budget", editedBudget);
                                onSave(editedBudget)
                            }}
                        >
                            Save
                        </button>
                        <button
                            type="button"
                            className="bg-gray-500 text-white px-4 py-2 rounded-md"
                            onClick={onCancel}
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