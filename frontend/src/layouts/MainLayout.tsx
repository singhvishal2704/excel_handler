import React from 'react'

type MainLayoutProps = {
  children: React.ReactNode
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-900 dark:text-white">
      <header className="bg-white shadow-md px-6 py-4 dark:bg-gray-800">
        <h1 className="text-2xl font-bold text-center">Excel Operations Tool</h1>
      </header>
      <main className="p-6 max-w-5xl mx-auto">{children}</main>
    </div>
  )
}

export default MainLayout
