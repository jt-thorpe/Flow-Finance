import Head from "next/head";
import Link from "next/link";
import { FaChartPie, FaMoneyBillWave, FaRegListAlt } from "react-icons/fa";

export default function Home() {
  return (
    <>
      <Head>
        <title>Flow-Finance | Budgeting Made Simple</title>
        <meta name="description" content="Take control of your finances with Flow-Finance." />
      </Head>
      <main className="flex flex-col items-center justify-center min-h-screen px-4 py-8 bg-gray-100">
        <section className="text-center max-w-3xl">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Take Control of Your Finances
          </h1>
          <p className="text-lg text-gray-700 mb-6">
            Flow-Finance helps you track income, expenses, and budgets with ease.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <button className="px-6 py-3 text-lg bg-blue-400 text-white rounded-lg hover:bg-green-500 w-36">Register</button>
            </Link>
            <Link href="/login">
              <button className="px-6 py-3 text-lg bg-green-400 text-white rounded-lg hover:bg-green-500 w-36">Login</button>
            </Link>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          <FeatureCard
            icon={<FaMoneyBillWave size={36} className="text-blue-500" />}
            title="Track Income & Expenses"
            description="Easily log your transactions and keep track of your finances."
          />
          <FeatureCard
            icon={<FaChartPie size={36} className="text-green-500" />}
            title="Visualise Your Budget"
            description="Understand your spending habits with insightful charts."
          />
          <FeatureCard
            icon={<FaRegListAlt size={36} className="text-yellow-500" />}
            title="Stay Organised"
            description="Categorise transactions and manage your finances efficiently."
          />
        </section>
      </main>
    </>
  );
}

const FeatureCard = ({ icon, title, description }: { icon: JSX.Element; title: string; description: string }) => {
  return (
    <div className="p-6 flex flex-col items-center text-center bg-white shadow-md rounded-2xl">
      {icon}
      <h3 className="text-xl font-semibold text-gray-800 mt-4">{title}</h3>
      <p className="text-gray-600 mt-2">{description}</p>
    </div>
  );
};
