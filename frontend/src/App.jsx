import React, { useState, useEffect } from 'react';

function App() {
  const [vehicles, setVehicles] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAdmin, setShowAdmin] = useState(false);

  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [category, setCategory] = useState('');
  const [price, setPrice] = useState('');
  const [quantity, setQuantity] = useState('');

  const fetchVehicles = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/vehicles');
      if (response.ok) {
        const data = await response.json();
        setVehicles(data);
      }
    } catch (error) {
      console.error("Error fetching inventory:", error);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  // Add Vehicle
  const handleAddVehicle = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/vehicles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          make,
          model,
          category,
          price: parseFloat(price),
          quantity: parseInt(quantity),
        }),
      });
      if (response.ok) {
        setMake(''); setModel(''); setCategory(''); setPrice(''); setQuantity('');
        fetchVehicles();
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Buy Vehicle (-1 stock)
  const handleBuy = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/vehicles/${id}/buy`, { method: 'POST' });
      if (res.ok) fetchVehicles();
    } catch (err) {
      console.error(err);
    }
  };

  // Restock Vehicle (+1 stock)
  const handleRestock = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/vehicles/${id}/restock`, { method: 'POST' });
      if (res.ok) fetchVehicles();
    } catch (err) {
      console.error(err);
    }
  };

  // Delete Vehicle
  const handleDelete = async (id) => {
    try {
      const res = await fetch(`http://localhost:8000/api/vehicles/${id}`, { method: 'DELETE' });
      if (res.ok) fetchVehicles();
    } catch (err) {
      console.error(err);
    }
  };

  const filteredVehicles = vehicles.filter(v => 
    v.make.toLowerCase().includes(searchQuery.toLowerCase()) ||
    v.model.toLowerCase().includes(searchQuery.toLowerCase()) ||
    v.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div style={{ backgroundColor: '#0f172a', minHeight: '100vh', color: '#f8fafc', padding: '2rem' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem' }}>
        <div>
          <h1 style={{ color: '#38bdf8', margin: 0, marginBottom: '0.75rem', fontSize: '2.25rem' }}>Car Dealership Inventory</h1>
          <p style={{ color: '#94a3b8', margin: 0, fontSize: '1rem' }}>Manage, search, and purchase vehicles in real-time</p>
        </div>
        <button style={{ backgroundColor: '#dc2626', color: '#fff', border: 'none', padding: '0.5rem 1rem', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Logout</button>
      </header>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <input
          type="text"
          placeholder="Search make, model, or category..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{ flex: 1, padding: '0.75rem', borderRadius: '8px', border: '1px solid #334155', backgroundColor: '#1e293b', color: '#fff' }}
        />
        <button 
          onClick={() => setShowAdmin(!showAdmin)}
          style={{ backgroundColor: '#334155', color: '#fff', border: 'none', padding: '0.75rem 1.25rem', borderRadius: '8px', cursor: 'pointer' }}
        >
          {showAdmin ? 'Hide Admin Controls' : 'Toggle Admin Controls'}
        </button>
      </div>

      {showAdmin && (
        <form onSubmit={handleAddVehicle} style={{ backgroundColor: '#1e293b', padding: '1.5rem', borderRadius: '8px', marginBottom: '2rem', display: 'grid', gridTemplateColumns: 'repeat( auto-fit, minmax(130px, 1fr) )', gap: '1rem' }}>
          <input placeholder="Make" value={make} onChange={e => setMake(e.target.value)} required style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <input placeholder="Model" value={model} onChange={e => setModel(e.target.value)} required style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <input placeholder="Category" value={category} onChange={e => setCategory(e.target.value)} required style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <input placeholder="Price" type="number" value={price} onChange={e => setPrice(e.target.value)} required style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <input placeholder="Quantity" type="number" value={quantity} onChange={e => setQuantity(e.target.value)} required style={{ padding: '0.5rem', borderRadius: '4px', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff' }} />
          <button type="submit" style={{ backgroundColor: '#16a34a', color: '#fff', border: 'none', padding: '0.5rem', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>Add Vehicle</button>
        </form>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1.5rem' }}>
        {filteredVehicles.map((car) => (
          <div key={car.id} style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px', padding: '1.5rem', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', textAlign: 'center' }}>
            <div>
              <span style={{ backgroundColor: '#0284c7', color: '#fff', fontSize: '0.75rem', padding: '0.25rem 0.5rem', borderRadius: '4px', textTransform: 'uppercase', fontWeight: 'bold' }}>{car.category}</span>
              <h2 style={{ fontSize: '1.35rem', marginTop: '0.85rem', marginBottom: '0.35rem', color: '#ffffff', fontWeight: 'bold' }}>{car.make} {car.model}</h2>
              <p style={{ color: '#38bdf8', fontSize: '1.25rem', fontWeight: 'bold', margin: '0.5rem 0' }}>${car.price.toLocaleString()}</p>
              <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>In Stock: <strong>{car.quantity}</strong> units</p>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1rem' }}>
              <button 
                onClick={() => handleBuy(car.id)} 
                disabled={car.quantity <= 0}
                style={{ width: '100%', backgroundColor: car.quantity > 0 ? '#2563eb' : '#64748b', color: '#fff', border: 'none', padding: '0.6rem', borderRadius: '6px', cursor: car.quantity > 0 ? 'pointer' : 'not-allowed', fontWeight: 'bold' }}
              >
                {car.quantity > 0 ? 'Buy Now' : 'Out of Stock'}
              </button>

              {showAdmin && (
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                  <button onClick={() => handleRestock(car.id)} style={{ flex: 1, backgroundColor: '#d97706', color: '#fff', border: 'none', padding: '0.4rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold' }}>+1 Restock</button>
                  <button onClick={() => handleDelete(car.id)} style={{ flex: 1, backgroundColor: '#dc2626', color: '#fff', border: 'none', padding: '0.4rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 'bold' }}>Delete</button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;