import { useState } from "react";
import BudgetItem from "../../types/BudgetItem";


const AddBudgetModal = ({
    onSave,
    onCancel,
}: {
    onSave: (budget: BudgetItem) => void;
    onCancel: () => void;
}) => {
    const [newBudget, setNewBudget] = useState<BudgetItem>({
        id: Date.now(), // temporary unique id; in a real app, use the id returned from the server
        category: "",
        amount: 0,
        spent: 0,
        remaining: 0,
        frequency: "",
    });

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
            <div className="bg-white p-6 rounded-md shadow-md w-full max-w-md">
                <h2 className="text-2xl font-bold mb-4">Add New Budget</h2>
                <form className="flex flex-col gap-4">
                    <label>
                        Category:
                        <input
                            type="text"
                            name="category"
                            value={newBudget.category}
                            onChange={(e) => setNewBudget({ ...newBudget, category: e.target.value })}
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Total Amount:
                        <input
                            type="number"
                            name="amount"
                            value={newBudget.amount}
                            onChange={(e) =>
                                setNewBudget({ ...newBudget, amount: parseFloat(e.target.value) })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Spent:
                        <input
                            type="number"
                            name="spent"
                            value={newBudget.spent}
                            onChange={(e) =>
                                setNewBudget({ ...newBudget, spent: parseFloat(e.target.value) })
                            }
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <label>
                        Frequency:
                        <input
                            type="text"
                            name="frequency"
                            value={newBudget.frequency}
                            onChange={(e) => setNewBudget({ ...newBudget, frequency: e.target.value })}
                            className="border border-gray-300 p-2 rounded-md w-full"
                        />
                    </label>
                    <div className="flex justify-end gap-2">
                        <button
                            type="button"
                            className="bg-green-500 text-white px-4 py-2 rounded-md"
                            onClick={() => onSave(newBudget)}
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

export default AddBudgetModal