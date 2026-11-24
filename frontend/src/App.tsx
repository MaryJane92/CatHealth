import { useEffect, useState } from "react";

interface HealthResponse {
  status: string;
  app: string;
  version: string;
}

function App() {
  const [apiStatus, setApiStatus] = useState<string>("—");

  useEffect(() => {
    fetch("/api/health")
      .then((r) => r.json())
      .then((data: HealthResponse) => setApiStatus(data.status))
      .catch(() => setApiStatus("недоступен"));
  }, []);

  return (
    <div>
      <h1>Cat Health Tracker</h1>
      <p>Мониторинг здоровья кошек</p>
      <p>
        API статус: <strong>{apiStatus}</strong>
      </p>
    </div>
  );
}

export default App;
