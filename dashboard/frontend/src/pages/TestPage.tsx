import { useEffect, useState } from "react";
import { getServices } from "../services/ServicesApi";

export default function TestPage() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    getServices().then((res) => setServices(res.data));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Services</h1>
      <ul>
        {services.map((s: any) => (
          <li key={s.id}>
            {s.name} — {s.status}
          </li>
        ))}
      </ul>
    </div>
  );
}
