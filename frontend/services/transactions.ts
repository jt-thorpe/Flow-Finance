export async function fetchTransactions(page: string, limit: string) {
    const params = new URLSearchParams({ page, limit });
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/transactions/list?${params.toString()}`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to fetch transactions");
    }

    const data = await response.json();
    
    if (!data.success) {
        throw new Error(data.message || "Failed to fetch transactions");
    }

    return {
        transactions: data.transactions,
        has_more: data.has_more
    };
}
