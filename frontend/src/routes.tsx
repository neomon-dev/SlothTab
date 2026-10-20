import { Routes, Route } from "react-router-dom"
import Dashboard from "./pages/Dashboard"
import Inbox from "./pages/Inbox"
import Activity from "./pages/Activity"
import Rules from "./pages/Rules"
import Settings from "./pages/Settings"
import DemoMode from "./pages/DemoMode"

const routes = (
  <Routes>
    <Route path="/" element={<Dashboard />} />
    <Route path="/inbox" element={<Inbox />} />
    <Route path="/activity" element={<Activity />} />
    <Route path="/rules" element={<Rules />} />
    <Route path="/settings" element={<Settings />} />
    <Route path="/demo" element={<DemoMode />} />
  </Routes>
)

export { routes }
export default routes