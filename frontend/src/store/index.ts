import { configureStore } from '@reduxjs/toolkit'
import excelReducer from './slices/excelSlice'

export const store = configureStore({
  reducer: {
    excel: excelReducer,
  },
})

// Types for dispatch and state
export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
