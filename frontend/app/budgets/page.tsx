'use client';

import { useContext, useEffect, useState } from "react";
import AddBudgetModal from "../../components/ui/AddBudgetModal";
import BudgetCard from "../../components/ui/BudgetCard";
import BudgetControls from "../../components/ui/BudgetControlBar";
import Navbar from "../../components/ui/NavBar";
import { AuthContext } from "../../context/AuthContext";
import useResponsive from "../../hooks/useResponsive";
import BudgetItem from "../../types/BudgetItem";


const Budgets = () => {
    const auth = useContext(AuthContext);
    const { isMobile, isNavOpen, setIsNavOpen } = useResponsive();
    const [userBudgetSummary, setUserBudgetSummary] = useState<BudgetItem[]>([]);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isRemoveMode, setIsRemoveMode] = useState(false);
    const [selectedBudgetIds, setSelectedBudgetIds] = useState<string[]>([]);

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

            const data = await response.json();
            
            if (!response.ok || !data.success) {
                console.error("Error loading budgets:", data.message);
                setUserBudgetSummary([]);
                return;
            }

            setUserBudgetSummary(data.budgets || []);
        } catch (error) {
            console.error("Error fetching budget data:", error);
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
    const toggleBudgetSelection = (id: string) => {
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
                    className={`fixed top-0 left-0 h-screen bg-white shadow-md transition-transform duration-300 z-[100] ${isMobile ? (isNavOpen ? "translate-x-0 w-64" : "-translate-x-full w-0") : "w-64 translate-x-0"
                        }`}
                >
                    <Navbar />
                </div>
                {isMobile && isNavOpen && (
                    <div
                        className="fixed inset-0 bg-black bg-opacity-50 z-[90]"
                        onClick={() => setIsNavOpen(false)}
                    ></div>
                )}
                <div className="flex-1 p-6 transition-all duration-300 md:ml-64 relative z-0">
                    <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl">
                        <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">Your Budgets</h1>
                        {/* Control Buttons for Adding and Removing */}
                        <div className="flex justify-center mb-4 gap-4">
                            <BudgetControls
                                onAdd={() => setIsAddModalOpen(true)}
                                onToggleRemove={toggleRemoveMode}
                                isRemoveMode={isRemoveMode}
                                selectedCount={selectedBudgetIds.length}
                                onConfirmRemove={confirmRemoval}
                            />
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


export default Budgets;
