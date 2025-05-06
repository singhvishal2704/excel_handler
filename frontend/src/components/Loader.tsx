import React from 'react'

const Loader: React.FC = () => (
  <div className="text-center py-8">
    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
    <p className="text-sm mt-2">Processing...</p>
  </div>
)

export default Loader
