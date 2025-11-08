import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import TestPage from "./pages/TestPage";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route
          path="/"
          element={
            <h1 className="text-2xl font-bold">Welcome to FastAPI-React-Lab</h1>
          }
        />
        <Route path="/test" element={<TestPage />} />
      </Route>
    </Routes>
  );
}

export default App;
