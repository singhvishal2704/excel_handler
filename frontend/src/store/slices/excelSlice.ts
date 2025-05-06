import { createSlice, PayloadAction } from '@reduxjs/toolkit'

interface ExcelState {
  sessionId: string | null
  data: any[]
  columns: string[]
  loading: boolean
  error: string | null
}

const initialState: ExcelState = {
  sessionId: null,
  data: [],
  columns: [],
  loading: false,
  error: null,
}

const excelSlice = createSlice({
  name: 'excel',
  initialState,
  reducers: {
    setSessionId: (state, action: PayloadAction<string>) => {
      state.sessionId = action.payload
    },
    setData: (state, action: PayloadAction<any[]>) => {
      state.data = action.payload
    },
    setColumns: (state, action: PayloadAction<string[]>) => {
      state.columns = action.payload
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload
    },
  },
})

export const { setSessionId, setData, setColumns, setLoading, setError } = excelSlice.actions
export default excelSlice.reducer
