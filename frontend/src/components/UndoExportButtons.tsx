import React from 'react'
import toast from 'react-hot-toast'
import { useAppDispatch, useAppSelector } from '../hooks/useTypedRedux'
import { exportExcel, postOperation } from '../services/api'
import { setData, setError, setLoading } from '../store/slices/excelSlice'

const UndoExportButtons: React.FC = () => {
  const sessionId = useAppSelector(state => state.excel.sessionId)
  const dispatch = useAppDispatch()

  const handleUndo = async () => {
    if (!sessionId) return
    dispatch(setLoading(true))
    try {
      const updated = await postOperation(sessionId, { operation: 'undo' })
      if (Array.isArray(updated) && updated.length > 0) {
        dispatch(setData(updated))
        toast.success('Undo successful.')
      } else {
        toast('Nothing to undo.', { icon: '⚠️' })
      }
    } catch (err: any) {
      dispatch(setError('Undo failed'))
      toast.error(err.response.data.message || 'No previous version available to undo.')
    } finally {
      dispatch(setLoading(false))
    }
  }

  const handleExport = async () => {
    if (!sessionId) return
    try {
      const blob = await exportExcel(sessionId)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'processed_data.xlsx')
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch (error) {
      toast.error('Failed to export Excel file')
    }
  }

  return (
    <div className="flex gap-4 mt-4">
      <button
        className="bg-yellow-500 text-white px-4 py-2 rounded"
        onClick={handleUndo}
      >
        Undo
      </button>
      <button
        className="bg-green-600 text-white px-4 py-2 rounded"
        onClick={handleExport}
      >
        Export
      </button>
    </div>
  )
}

export default UndoExportButtons
