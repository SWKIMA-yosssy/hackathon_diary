"use client";

interface TestButtonsProps {
  user:
    | {
        name?: string | null;
        email?: string | null;
      }
    | undefined;
}

export default function TestButtons({ user }: TestButtonsProps) {
  return (
    <div>
      <div>
        <p>Welcome, {user?.name}!</p>
        <p>{user?.email}</p>
      </div>

      <div>
        <button
          onClick={async () => {
            try {
              const res = await fetch("/api/bff/articles", { method: "GET" });
              const data = await res.json();
              alert("Articles (匿名OK): " + JSON.stringify(data, null, 2));
            } catch (error) {
              alert("Error: " + error);
            }
          }}>
          Load Articles (Public)
        </button>

        <button
          onClick={async () => {
            try {
              const res = await fetch("/api/bff/api/secure-whoami", { method: "GET" });
              const data = await res.json();
              alert("Whoami (認証必要): " + JSON.stringify(data, null, 2));
            } catch (error) {
              alert("Error: " + error);
            }
          }}>
          Whoami (Auth Required)
        </button>

        <button
          onClick={async () => {
            try {
              const res = await fetch("/api/bff/health", { method: "GET" });
              const data = await res.json();
              alert("Health Check: " + JSON.stringify(data, null, 2));
            } catch (error) {
              alert("Error: " + error);
            }
          }}>
          Health Check
        </button>
      </div>
    </div>
  );
}
