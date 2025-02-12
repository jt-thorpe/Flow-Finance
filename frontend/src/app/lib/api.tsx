export async function fetchTransactions(page: number) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/transactions/get-by?page=${page}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
    });


    if (!response.ok) {
        throw new Error("Failed to fetch transactions");
    }

    return response.json();
}
