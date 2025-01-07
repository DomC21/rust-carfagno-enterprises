import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-brand-dark p-6 border-b border-brand-gold">
      <div className="container mx-auto">
        <h1 className="text-4xl font-bold brand-gold">Rust: A Tool by Carfagno Enterprises</h1>
        <p className="text-gray-400 mt-2">Advanced Stock Analysis and Trading Insights</p>
      </div>
    </header>
  );
};

export default Header;
