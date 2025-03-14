import React from "react";

interface BudgetControlsProps {
  onAdd: () => void;
  onToggleRemove: () => void;
  isRemoveMode: boolean;
  selectedCount: number;
  onConfirmRemove: () => void;
}

const BudgetControls: React.FC<BudgetControlsProps> = ({
  onAdd,
  onToggleRemove,
  isRemoveMode,
  selectedCount,
  onConfirmRemove,
}) => {
  return (
    <div className="flex justify-center mb-4 gap-4">
      <button
        onClick={onAdd}
        className="bg-green-400 text-white px-4 py-2 rounded-md"
      >
        +
      </button>
      <button
        onClick={onToggleRemove}
        className="bg-green-400 text-white px-4 py-2 rounded-md"
      >
        {isRemoveMode ? "Cancel" : "-"}
      </button>
      {isRemoveMode && selectedCount > 0 && (
        <button
          onClick={onConfirmRemove}
          className="bg-red-700 text-white px-4 py-2 rounded-md"
        >
          Remove
        </button>
      )}
    </div>
  );
};

export default BudgetControls;
