const OverviewCard = ({ title, amount, color }: { title: string; amount: number | null; color: string }) => (
    <div role="region" aria-label={title} className="bg-white p-6 rounded-2xl shadow-md text-center">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className={`text-xl font-bold ${color}`}>£{(amount ?? 0).toFixed(2)}</p>
    </div>
);

export default OverviewCard