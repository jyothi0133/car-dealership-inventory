import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api';
import { AuthContext } from '../AuthContext';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
  const [message, setMessage] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (isRegistering) {
      try {
        const username = email.split('@')[0];
        await API.post('/auth/register', { username, email, password });
        setMessage('Registration successful! Please log in.');
        setIsRegistering(false);
      } catch (err) {
        setMessage(err.response?.data?.detail || 'Registration failed');
      }
    } else {
      try {
        const res = await API.post('/auth/login', { email, password });
        login({ email }, res.data.access_token);
        navigate('/');
      } catch (err) {
        setMessage(err.response?.data?.detail || 'Login failed');
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <form onSubmit={handleSubmit} className="p-6 bg-white rounded-lg shadow-md w-80 flex flex-col gap-3">
        <h2 className="text-2xl font-bold text-center text-gray-800">
          {isRegistering ? 'Register' : 'Login'}
        </h2>
        {message && <p className="text-blue-600 text-sm text-center font-medium">{message}</p>}
        
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" 
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500" 
          required 
        />
        <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 font-semibold transition">
          {isRegistering ? 'Register Account' : 'Login'}
        </button>
        <button 
          type="button" 
          onClick={() => { setIsRegistering(!isRegistering); setMessage(''); }}
          className="w-full text-xs text-gray-600 hover:underline text-center mt-1"
        >
          {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
        </button>
      </form>
    </div>
  );
}