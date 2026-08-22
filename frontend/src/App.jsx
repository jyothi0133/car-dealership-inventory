import React, { useState, useEffect } from 'react';

const API_BASE = 'http://127.0.0.1:8000/api';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [vehicles, setVehicles] = useState([]);
  const [query, setQuery] = useState('');
  const [isAdmin, setIsAdmin] = useState(false);

  // New vehicle state
  const [newVehicle, setNewVehicle] = useState({ make: '', model: '', category: '', price: '', quantity: '' });

  useEffect(() => {
    if (token) fetchVehicles();
  }, [token, query]);

  const handleAuth = async (isRegister = false) => {
    const endpoint = isRegister ? '/auth/register' : '/auth/login';
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok) {
        if (!isRegister) {
          localStorage.setItem('token', data.access_token);
          setToken(data.access_token);
          // Simple admin check based on email domain or test flag
          if (email.includes('admin')) setIsAdmin(true);
        } else {
          alert('Registered successfully! Please login.');
        }
      } else {
        alert(data.detail || 'Authentication failed');
      }
    } catch (err) {
      alert('Error connecting to backend server');
    }
  };

  const fetchVehicles = async () => {
    const url = query ? `${API_BASE}/vehicles/search?query=${query}` : `${API_BASE}/vehicles`;
    const res = await fetch(url);
    if (res.ok) setVehicles(await res.json());
  };

  const handlePurchase = async (id) => {
    const res = await fetch(`${API_BASE}/vehicles/${id}/purchase`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      alert('Purchase successful!');
      fetchVehicles();
    } else {
      const err = await res.json();
      alert(err.detail || 'Purchase failed');
    }
  };

  const handleAddVehicle = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API_BASE}/vehicles`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        ...newVehicle,
        price: parseFloat(newVehicle.price),
        quantity: parseInt(newVehicle.quantity)
      })
    });
    if (res.ok) {
      alert('Vehicle added successfully!');
      setNewVehicle({ make: '', model: '', category: '', price: '', quantity: '' });
      fetchVehicles();
    } else {
      alert('Only admins can add vehicles');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this vehicle?')) return;
    const res = await fetch(`${API_BASE}/vehicles/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) {
      fetchVehicles();
    } else {
      alert('Admin privileges required to delete');
    }
  };

  const handleRestock = async (id) => {
    const qty = prompt('Enter quantity to add:');
    if (!qty) return;
    const res = await fetch(`${API_BASE}/vehicles/${id}/restock`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ quantity: parseInt(qty) })
    });
    if (res.ok) {
      fetchVehicles();
    } else {
      alert('Admin privileges required to restock');
    }
  };

  if (!token) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
        <div className="bg-slate-800 p-8 rounded-2xl shadow-2xl border border-slate-700 w-full max-w-md">
          <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 mb-6 text-center">
            Dealership Portal
          </h1>
          <div className="space-y-4">
            <input
              type="email"
              placeholder="Email"
              className="w-full p-3 bg-slate-700 rounded-lg text-white border border-slate-600 focus:outline-none focus:border-blue-500"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <input
              type="password"
              placeholder="Password"
              className="w-full p-3 bg-slate-700 rounded-lg text-white border border-slate-600 focus:outline-none focus:border-blue-500"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div className="flex gap-4 pt-2">
              <button
                onClick={() => handleAuth(false)}
                className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-bold py-3 rounded-lg transition"
              >
                Login
              </button>
              <button
                onClick={() => handleAuth(true)}
                className="flex-1 bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 rounded-lg border border-slate-500 transition"
              >
                Register
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <header className="flex justify-between items-center pb-6 border-b border-slate-800">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent">
              Car Dealership Inventory
            </h1>
            <p className="text-slate-400 text-sm">Manage, search, and purchase vehicles in real-time</p>
          </div>
          <button
            onClick={() => {
              localStorage.removeItem('token');
              setToken('');
            }}
            className="bg-red-500/20 text-red-400 hover:bg-red-500 hover:text-white px-4 py-2 rounded-lg font-medium transition"
          >
            Logout
          </button>
        </header>

        {/* Controls Bar */}
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <input
            type="text"
            placeholder="Search make, model, or category..."
            className="flex-1 min-w-[280px] p-3 bg-slate-800 rounded-xl border border-slate-700 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button
            onClick={() => setIsAdmin(!isAdmin)}
            className={`px-4 py-3 rounded-xl font-bold text-sm transition ${
              isAdmin ? 'bg-amber-500 text-slate-900' : 'bg-slate-800 text-slate-300 border border-slate-700'
            }`}
          >
            {isAdmin ? 'Admin Mode: Active' : 'Toggle Admin Controls'}
          </button>
        </div>

        {/* Admin Add Vehicle Panel */}
        {isAdmin && (
          <form onSubmit={handleAddVehicle} className="bg-slate-800/60 p-6 rounded-2xl border border-amber-500/30 space-y-4">
            <h3 className="text-lg font-semibold text-amber-400">Add New Vehicle (Admin)</h3>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              <input placeholder="Make" className="p-2 bg-slate-700 rounded text-white" value={newVehicle.make} onChange={e => setNewVehicle({...newVehicle, make: e.target.value})} required />
              <input placeholder="Model" className="p-2 bg-slate-700 rounded text-white" value={newVehicle.model} onChange={e => setNewVehicle({...newVehicle, model: e.target.value})} required />
              <input placeholder="Category" className="p-2 bg-slate-700 rounded text-white" value={newVehicle.category} onChange={e => setNewVehicle({...newVehicle, category: e.target.value})} required />
              <input placeholder="Price" type="number" className="p-2 bg-slate-700 rounded text-white" value={newVehicle.price} onChange={e => setNewVehicle({...newVehicle, price: e.target.value})} required />
              <input placeholder="Stock Qty" type="number" className="p-2 bg-slate-700 rounded text-white" value={newVehicle.quantity} onChange={e => setNewVehicle({...newVehicle, quantity: e.target.value})} required />
            </div>
            <button type="submit" className="bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold px-6 py-2 rounded-lg transition">
              Add Vehicle
            </button>
          </form>
        )}

        {/* Inventory Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {vehicles.map((v) => (
            <div key={v.id} className="bg-slate-800 rounded-2xl p-6 border border-slate-700 shadow-xl flex flex-col justify-between hover:border-slate-600 transition">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <span className="text-xs uppercase font-semibold tracking-wider text-blue-400 bg-blue-500/10 px-2.5 py-1 rounded-full">
                    {v.category}
                  </span>
                  <span className={`text-xs font-bold px-2 py-1 rounded ${v.quantity > 0 ? 'bg-emerald-500/10 text-emerald-400' : 'bg-red-500/10 text-red-400'}`}>
                    {v.quantity > 0 ? `${v.quantity} in stock` : 'Out of Stock'}
                  </span>
                </div>
                <h2 className="text-2xl font-bold text-white mb-1">{v.make} {v.model}</h2>
                <p className="text-2xl font-extrabold text-teal-400 my-3">${v.price.toLocaleString()}</p>
              </div>

              <div className="space-y-2 pt-4 border-t border-slate-700/50">
                <button
                  onClick={() => handlePurchase(v.id)}
                  disabled={v.quantity <= 0}
                  className="w-full bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 disabled:text-slate-500 text-white font-bold py-2.5 rounded-xl transition"
                >
                  Purchase Vehicle
                </button>

                {isAdmin && (
                  <div className="flex gap-2 pt-2">
                    <button
                      onClick={() => handleRestock(v.id)}
                      className="flex-1 bg-amber-500/20 text-amber-300 hover:bg-amber-500 hover:text-slate-900 py-1.5 rounded-lg text-sm font-semibold transition"
                    >
                      Restock
                    </button>
                    <button
                      onClick={() => handleDelete(v.id)}
                      className="flex-1 bg-red-500/20 text-red-300 hover:bg-red-500 hover:text-white py-1.5 rounded-lg text-sm font-semibold transition"
                    >
                      Delete
                    </button>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}