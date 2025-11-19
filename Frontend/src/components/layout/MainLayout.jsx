import { Outlet } from "react-router-dom";
import FloatingMenu from "./FloatingMenu";

export default function MainLayout() {
  return (
    <div className="min-h-screen flex flex-col bg-white">
      <main className="flex-1">
        <Outlet />
      </main>
      <FloatingMenu />
    </div>
  );
}
