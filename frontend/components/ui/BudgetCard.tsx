import { useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer } from "recharts";
import BudgetItem from "../../app/types/BudgetItem";
import EditBudgetModal from "./EditBudgetModal";

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

export default BudgetCard