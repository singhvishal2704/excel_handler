import React from 'react'
import { useAppSelector } from '../hooks/useTypedRedux'

const DataTable: React.FC = () => {
  const data = useAppSelector(state => state.excel.data)
  const columns = useAppSelector(state => state.excel.columns)

  if (!data || data.length === 0) return <p className="text-gray-500">No data available</p>

  return (
    <div className="overflow-x-auto mt-4">
      <table className="min-w-full border border-gray-300 text-sm">
        <thead>
          <tr className="bg-gray-200">
            {columns.map((col) => (
              <th key={col} className="border px-4 py-2">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {columns.map(col => (
                <td key={col} className="border px-4 py-2">{row[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DataTable
