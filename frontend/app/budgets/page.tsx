'use client';

import { useContext, useEffect, useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import Navbar from "../../components/ui/NavBar";
import { AuthContext } from "../../context/AuthContext";


interface BudgetItem {
    id: number; // Ideally a unique ID for each budget.
    category: string;
    amount: number;
    spent: number;
    remaining: number;
    frequency: string;
}

const Budgets = () => {
    const auth = useContext(AuthContext);
    const [userBudgetSummary, setUserBudgetSummary] = useState<BudgetItem[]>([]);
    const [isMobile, setIsMobile] = useState(false);
    const [isNavOpen, setIsNavOpen] = useState(false);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isRemoveMode, setIsRemoveMode] = useState(false);
    const [selectedBudgetIds, setSelectedBudgetIds] = useState<number[]>([]);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 768);
            if (window.innerWidth >= 768) setIsNavOpen(false);
        };
        handleResize();
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    useEffect(() => {
        if (auth?.user?.user_id) {
            fetchUserBudgets();
        }
    }, [auth?.user]);

    const fetchUserBudgets = async () => {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/budgets/load`, {
                method: "GET",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
            });

            if (response.status === 401) {
                window.location.href = "/login";
                return;
            }

            if (response.ok) {
                const data = await response.json();
                // Make sure each budget has a unique id. Adjust based on your data.
                setUserBudgetSummary(data || []);
            }
        } catch (error) {
            console.error("Error fetching budget data", error);
            setUserBudgetSummary([]);
        }
    };

    // Handler for adding a new budget
    const handleAddBudget = (newBudget: BudgetItem) => {
        setUserBudgetSummary([...userBudgetSummary, newBudget]);
        setIsAddModalOpen(false);
    };

    // Toggle removal mode on/off
    const toggleRemoveMode = () => {
        setIsRemoveMode((prev) => !prev);
        if (isRemoveMode) {
            // Clear any selected budgets when leaving removal mode
            setSelectedBudgetIds([]);
        }
    };

    // Toggle selection of a budget (by id) for removal
    const toggleBudgetSelection = (id: number) => {
        if (selectedBudgetIds.includes(id)) {
            setSelectedBudgetIds(selectedBudgetIds.filter((bid) => bid !== id));
        } else {
            setSelectedBudgetIds([...selectedBudgetIds, id]);
        }
    };

    // Confirm removal of selected budgets
    const confirmRemoval = () => {
        // Optionally show a confirmation modal before deleting.
        const updatedBudgets = userBudgetSummary.filter(
            (budget) => !selectedBudgetIds.includes(budget.id)
        );
        setUserBudgetSummary(updatedBudgets);
        setSelectedBudgetIds([]);
        setIsRemoveMode(false);
    };

    return (
        <main className="flex flex-col items-center min-v-screen px-4 py-8 bg-gray-100">
            <div className="flex min-h-screen bg-gray-100 relative">
                <div
                    className={`fixed top-0 left-0 h-screen bg-white shadow-md transition-transform duration-300 ${isMobile ? (isNavOpen ? "translate-x-0 w-64" : "-translate-x-full w-0") : "w-64 translate-x-0"
                        }`}
                >
                    <Navbar />
                </div>
                {isMobile && isNavOpen && (
                    <div
                        className="fixed inset-0 bg-black bg-opacity-50 z-40"
                        onClick={() => setIsNavOpen(false)}
                    ></div>
                )}
                <div className="flex-1 p-6 transition-all duration-300 md:ml-64">
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Your Budgets</h1>
                        {/* Control Buttons for Adding and Removing */}
                        <div className="flex justify-end mb-4 gap-4">
                            <button
                                onClick={() => setIsAddModalOpen(true)}
                                className="bg-blue-500 text-white px-4 py-2 rounded-md"
                            >
                                +
                            </button>
                            <button
                                onClick={toggleRemoveMode}
                                className="bg-blue-500 text-white px-4 py-2 rounded-md"
                            >
                                {isRemoveMode ? "Cancel" : "-"}
                            </button>
                            {isRemoveMode && selectedBudgetIds.length > 0 && (
                                <button
                                    onClick={confirmRemoval}
                                    className="bg-red-700 text-white px-4 py-2 rounded-md"
                                >
                                    Remove
                                </button>
                            )}
                        </div>
                        <div className="flex flex-col gap-6">
                            {userBudgetSummary.length > 0 ? (
                                userBudgetSummary.map((budget, index) => (
                                    <BudgetCard
                                        key={budget.id}
                                        budget={budget}
                                        isMobile={isMobile}
                                        isRemoveMode={isRemoveMode}
                                        isSelected={selectedBudgetIds.includes(budget.id)}
                                        toggleSelection={() => toggleBudgetSelection(budget.id)}
                                    />
                                ))
                            ) : (
                                <p className="text-center text-gray-500">No budgets available.</p>
                            )}
                        </div>
                    </section>
                </div>
            </div>

            {isAddModalOpen && (
                <AddBudgetModal
                    onSave={handleAddBudget}
                    onCancel={() => setIsAddModalOpen(false)}
                />
            )}
        </main>
    );
};

// A modified BudgetCard that supports removal mode and editing
const BudgetCard = ({
    budget,
    isMobile,
    isRemoveMode,
    isSelected,
    toggleSelection,
}: {
    budget: BudgetItem;
    isMobile: boolean;
    isRemoveMode: boolean;
    isSelected: boolean;
    toggleSelection: () => void;
}) => {
    const [isEditModalOpen, setEditModalOpen] = useState(false);
    const [editedBudget, setEditedBudget] = useState({ ...budget });

    // In removal mode, clicking toggles selection; otherwise, open the edit modal.
    const handleCardClick = () => {
        if (isRemoveMode) {
            toggleSelection();
        } else {
            setEditModalOpen(true);
        }
    };

    // Prepare pie chart data and colors
    const pieData = [
        { name: "Spent", value: budget.spent },
        { name: "Remaining", value: budget.amount - budget.spent },
    ];
    const COLOURS = ["#FF6B6B", "#4CAF50"];

    return (
        <div
            className={`relative bg-white p-6 rounded-2xl shadow-md cursor-pointer ${isRemoveMode && isSelected ? "border-2 border-red-500" : ""
                } ${isMobile ? "flex flex-col items-center" : "flex items-center w-full"}`}
            onClick={handleCardClick}
        >
            <div className={`${isMobile ? "w-full mb-4 flex justify-center" : "w-1/4 flex justify-center"}`}>
                <ResponsiveContainer width={100} height={100}>
                    <PieChart>
                        <Pie
                            data={pieData}
                            cx="50%"
                            cy="100%"
                            startAngle={180}
                            endAngle={0}
                            innerRadius={30}
                            outerRadius={45}
                            paddingAngle={2}
                            dataKey="value"
                        >
                            {pieData.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={COLOURS[index % COLOURS.length]} />
                            ))}
                        </Pie>
                    </PieChart>
                </ResponsiveContainer>
            </div>
            <div className={`${isMobile ? "w-full text-center" : "w-1/4 pl-4"}`}>
                <h2 className="text-lg font-semibold">{budget.category}</h2>
                <p className="text-gray-700">Total: £{budget.amount.toFixed(2)}</p>
                <p className="text-red-500">Spent: £{budget.spent.toFixed(2)}</p>
                <p className="text-green-500">Remaining: £{budget.remaining.toFixed(2)}</p>
                <p className="text-gray-500 text-sm">Frequency: {budget.frequency}</p>
            </div>
            <div
                className={`${isMobile
                    ? "w-full mt-4 bg-gray-100 p-3 rounded-md text-gray-600 text-sm"
                    : "w-2/4 bg-gray-100 p-3 rounded-md text-gray-600 text-sm ml-4"
                    }`}
            >
                <ul>
                    <li>• There are {0} remaining days of this budget.</li>
                    <li>• There are {0} scheduled payments remaining for the month.</li>
                </ul>
            </div>

            {isEditModalOpen && !isRemoveMode && (
                <EditBudgetModal
                    budget={editedBudget}
                    onSave={(updatedBudget) => {
                        // Replace with your update logic (API call or state update)
                        console.log("Updated Budget", updatedBudget);
                        setEditModalOpen(false);
                    }}
                    onCancel={() => setEditModalOpen(false)}
                />
            )}
            {!isEditModalOpen && (
                <button
                    onClick={handleCardClick}
                    className="absolute inset-0 w-full h-full opacity-0"
                ></button>
            )}
        </div>
    );
};

// Modal for adding a new budget
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

// Modal for editing an existing budget (similar to the Add modal)
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
                            className="bg-green-500 text-white px-4 py-2 rounded-md"
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

export default Budgets;
