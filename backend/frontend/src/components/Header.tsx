import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-gray-900 text-white p-6">
      <div className="container mx-auto">
        <h1 className="text-3xl font-bold">Rust: A Tool by Carfagno Enterprises</h1>
        <p className="text-gray-400 mt-2">Advanced Stock Analysis and Trading Insights</p>
      </div>
    </header>
  );
};

export default Header;
