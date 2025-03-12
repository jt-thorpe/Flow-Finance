export async function fetchTransactions(page: string, limit: string) {
    const params = new URLSearchParams({ page, limit });
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/transactions/get-by?${params.toString()}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
    });


    if (!response.ok) {
        throw new Error("Failed to fetch transactions");
    }

    return response.json();
}
