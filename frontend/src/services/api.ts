import axiosClient from './axiosClient'

interface APIResponse<T> {
  success: boolean
  message: string
  data: T
}

// 1. Upload Excel File
export const uploadExcel = async (file: File): Promise<{
  session_id: string
  columns: string[]
}> => {
  const formData = new FormData()
  formData.append('file', file)

  const res = await axiosClient.post<APIResponse<{ session_id: string; columns: string[] }>>(
    '/api/v1/upload/',
    formData,
    {
      headers: { 'Content-Type': 'multipart/form-data' },
    }
  )

  if (!res.data.success) {
    throw new Error(res.data.message || 'Upload failed')
  }

  return res.data.data
}

// 2. Get Processed Data
export const getProcessedData = async (sessionId: string): Promise<any[]> => {
  const res = await axiosClient.get<APIResponse<any[]>>('/api/v1/get-data/', {
    params: { session_id: sessionId },
  })

  if (!res.data.success) {
    throw new Error(res.data.message || 'Fetching data failed')
  }

  return res.data.data
}

// 3. Post Operation
export const postOperation = async (
  sessionId: string,
  payload: { operation: string; [key: string]: any }
): Promise<any[]> => {
  const res = await axiosClient.post<APIResponse<any[]>>('/api/v1/operate/', {
    session_id: sessionId,
    ...payload,
  })

  if (!res.data.success) {
    throw new Error(res.data.message || 'Operation failed')
  }

  return res.data.data
}

// 4. Export Processed Excel
export const exportExcel = async (sessionId: string): Promise<Blob> => {
  const res = await axiosClient.get('/api/v1/export/', {
    params: { session_id: sessionId },
    responseType: 'blob',
  })

  return res.data // No need to wrap in success here if always downloading
}
