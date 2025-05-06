import React from 'react'
import MainLayout from './layouts/MainLayout'
import FileUploader from './components/FileUploader'
import OperationsPanel from './components/OperationsPanel'
import UndoExportButtons from './components/UndoExportButtons'
import Loader from './components/Loader'
import { useAppSelector } from './hooks/useTypedRedux'
import { Toaster } from 'react-hot-toast'


function App() {
  const loading = useAppSelector(state => state.excel.loading)

  return (
    <>
    <MainLayout>
      <FileUploader />
      <hr className="my-6" />
      {loading ? <Loader /> : <OperationsPanel />}
      <UndoExportButtons />
    </MainLayout>
    <Toaster />
    </>
  )
}

export default App
