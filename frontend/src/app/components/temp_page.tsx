import Navbar from '../components/NavBar';

const PageTemplate = ({ title }: { title: string }) => {
    return (
        <main className="flex min-h-screen bg-gray-100">
            {/* Sidebar Navigation */}
            <div className="w-64 hidden md:block">
                <Navbar />
            </div>

            {/* Main Content */}
            <div className="flex-1 p-6">
                <section className="bg-white shadow-md rounded-2xl p-8 w-full max-w-4xl mx-auto">
                    <h1 className="text-3xl font-bold text-center mb-6 text-gray-900">{title}</h1>
                    <p className="text-center text-gray-600">This page is under construction.</p>
                </section>
            </div>
        </main>
    );
};

export function Budgets() { return <PageTemplate title="Budgets" />; }
export function Insights() { return <PageTemplate title="Insights" />; }
export function Settings() { return <PageTemplate title="Settings" />; }
export function Transactions() { return <PageTemplate title="Transactions" />; }
