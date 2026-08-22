import { useState, useEffect, useContext } from 'react';
import API from '../api';
import { AuthContext } from '../AuthContext';

export default function Dashboard() {
  const [vehicles, setVehicles] = useState([]);
  const [search, setSearch] = useState('');
  const [makeFilter, setMakeFilter] = useState('');
  const { logout } = useContext(AuthContext);

  const fetchVehicles = async () => {
    try {
      let endpoint = '/vehicles';
      let params = {};

      if (search.trim()) {
        endpoint = '/vehicles/search';
        params = { query: search };
      } else if (makeFilter.trim()) {
        params = { make: makeFilter };
      }

      const res = await API.get(endpoint, { params });
      setVehicles(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, [search, makeFilter]);

  const handleBuy = async (vehicleId) => {
    try {
      await API.post('/sales', { vehicle_id: vehicleId, quantity: 1 });
      fetchVehicles();
    } catch (err) {
      alert(err.response?.data?.detail || 'Purchase failed');
    }
  };

  const handleRestock = async (vehicleId) => {
    try {
      await API.post(`/vehicles/${vehicleId}/restock`, { quantity: 10 });
      fetchVehicles();
    } catch (err) {
      alert(err.response?.data?.detail || 'Restock failed');
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto text-center">
      <h1 className="text-4xl font-bold mb-4">Car Dealership Inventory</h1>
      <button onClick={logout} className="mb-6 px-4 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition">
        Logout
      </button>
      
      <div className="flex justify-center gap-4 mb-8">
        <input 
          type="text" 
          placeholder="Search model/make..." 
          value={search} 
          onChange={(e) => setSearch(e.target.value)}
          className="border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <input 
          type="text" 
          placeholder="Filter by Make (e.g. Toyota)" 
          value={makeFilter} 
          onChange={(e) => setMakeFilter(e.target.value)}
          className="border p-2 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {vehicles.map((v) => (
          <div key={v.id} className="border p-6 rounded-lg shadow-sm bg-white">
            <h2 className="text-2xl font-bold text-gray-800">{v.make} {v.model}</h2>
            <p className="text-gray-600">Category: {v.category}</p>
            <p className="text-xl font-semibold text-green-600 mt-2">${v.price}</p>
            <p className="mt-1 font-medium text-gray-700">Stock: {v.quantity}</p>
            
            <div className="flex justify-center gap-3 mt-4">
              <button 
                onClick={() => handleBuy(v.id)} 
                disabled={v.quantity <= 0}
                className={`px-4 py-2 rounded text-white font-medium transition ${
                  v.quantity > 0 ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-400 cursor-not-allowed'
                }`}
              >
                {v.quantity > 0 ? 'Buy 1 Unit' : 'Out of Stock'}
              </button>
              
              <button 
                onClick={() => handleRestock(v.id)}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded transition"
              >
                + Restock (10)
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}