import './css/App.css';
import Home from './pages/Home';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  // Correzione qui
import 'primereact/resources/themes/bootstrap4-light-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import Login from './pages/Login';
import ProtectedRoute from './basic/Protected';

function App() {
  return (
    <Router>
      <Routes> 
        <Route path="/" element={<Login />} />
        {/* La pagina Home è protetta */}
        <Route 
          path="/home" 
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;