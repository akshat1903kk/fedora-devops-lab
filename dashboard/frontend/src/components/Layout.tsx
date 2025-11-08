import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <nav className="bg-gray-800 p-4 flex gap-4 text-sm font-medium">
        <Link to="/" className="hover:text-blue-400">
          Home
        </Link>
        <Link to="/test" className="hover:text-blue-400">
          Services
        </Link>
      </nav>

      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}
