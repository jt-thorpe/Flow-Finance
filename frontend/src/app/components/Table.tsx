const Table = ({ headers, data }: { headers: string[], data: any[][] }) => (
    <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left">
            <thead>
                <tr className="bg-gray-200">
                    {headers.map((header, index) => <th key={index} className="p-3 font-semibold">{header}</th>)}
                </tr>
            </thead>
            <tbody>
                {data.length > 0 ? (
                    data.map((row, rowIndex) => (
                        <tr key={rowIndex} className="border-t">
                            {row.map((cell, cellIndex) => <td key={cellIndex} className="p-3">{cell}</td>)}
                        </tr>
                    ))
                ) : (
                    <tr>
                        <td colSpan={headers.length} className="p-3 text-center text-gray-500">No data available.</td>
                    </tr>
                )}
            </tbody>
        </table>
    </div>
);

export default Table