import React from 'react';

interface TableViewProps {
  tableData: any[];
}

const TableView = ({ tableData }: TableViewProps) => {
  const tableHeaders = tableData.length > 0 ? Object.keys(tableData[0]) : [];

  return (
    <div className="overflow-x-auto  text-Pri-Dark ">
      {tableData.length !== 0 && (
        <div className="min-w-full">
          <div className="text-2xl font-semibold text-Pri-Dark mb-4">
            🚀 My Result
          </div>
          <table className="min-w-full border-collapse">
            <thead>
              <tr className="0 font-bold text-Pri-Dark">
                {tableHeaders.map((header) => (
                  <th key={header} className="p-2 border">
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {tableData.map((row, index) => (
                <tr key={index} className="border-b">
                  {tableHeaders.map((header) => (
                    <td key={`${index}-${header}`} className="p-2 border">
                      {row[header]}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default TableView;
