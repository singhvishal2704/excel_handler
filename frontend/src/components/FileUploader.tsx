import React, { useState, useRef } from 'react'
import { useAppDispatch } from '../hooks/useTypedRedux'
import {
  setSessionId,
  setColumns,
  setLoading,
  setError,
  setData,
} from '../store/slices/excelSlice'
import { uploadExcel, getProcessedData } from '../services/api'
import toast from 'react-hot-toast'

const FileUploader: React.FC = () => {
  const dispatch = useAppDispatch()
  const [file, setFile] = useState<File | null>(null)
  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const validateFile = (f: File): boolean => {
    const isExcel = f.name.endsWith('.xlsx') || f.name.endsWith('.xls')
    const isUnderLimit = f.size <= 5 * 1024 * 1024 // 5MB
    if (!isExcel) {
      setErrorMsg('Invalid file type. Please upload an Excel file (.xlsx or .xls).')
      return false
    }
    if (!isUnderLimit) {
      setErrorMsg('File is too large. Maximum size allowed is 5MB.')
      return false
    }
    setErrorMsg(null)
    return true
  }

  const handleFile = (selected: File) => {
    if (validateFile(selected)) {
      setFile(selected)
    } else {
      setFile(null)
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    if (e.dataTransfer.files?.[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
  }

  const handleUpload = async () => {
    if (!file) return
    try {
      dispatch(setLoading(true))
      const response = await uploadExcel(file)
      const sessionId = response.session_id
      dispatch(setSessionId(sessionId))
      dispatch(setColumns(response.columns))

      const data = await getProcessedData(sessionId)
      dispatch(setData(data))

      toast.success('File uploaded and data loaded successfully.')
    } catch (error: any) {
      dispatch(setError('Upload failed'))
      setErrorMsg('Upload failed. Please try again.')
      toast.error('Upload failed. Please try again.')
    } finally {
      dispatch(setLoading(false))
    }
  }

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition ${
          file ? 'border-green-400 bg-green-50' : 'border-gray-400 bg-gray-50 hover:bg-gray-100'
        }`}
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
      >
        {file ? (
          <p className="text-sm text-green-700">
            Selected File: <strong>{file.name}</strong>
          </p>
        ) : (
          <p className="text-sm text-gray-500">
            Drag and drop your Excel file here, or{' '}
            <span className="text-blue-600 underline">click to select</span>
          </p>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept=".xlsx,.xls"
          className="hidden"
          onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        />
      </div>

      {errorMsg && <p className="text-red-500 text-sm">{errorMsg}</p>}

      <button
        onClick={handleUpload}
        className="bg-primary text-white px-4 py-2 rounded disabled:opacity-50"
        disabled={!file || !!errorMsg}
      >
        Upload Excel
      </button>
    </div>
  )
}

export default FileUploader