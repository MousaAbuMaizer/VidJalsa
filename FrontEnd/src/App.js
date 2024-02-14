import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import MainPage from "./pages/MainPage";
import PreviewPage from "./pages/PreviewPage";
import LoadingPage from "./pages/LoadingPage";
import OutputPage from './pages/OutputPage';

import StarsBackground from './components/StarsBackground';

function App() {
  return (
    <div className="App">
      <Router>
        <ToastContainer />
        <StarsBackground />
        <Routes>
          <Route index element={<MainPage />} />
          <Route path="/preview" element={<PreviewPage />} />
          <Route path="/loading" element={<LoadingPage />} />
          <Route path="/output" element={<OutputPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;

