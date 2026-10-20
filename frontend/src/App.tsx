import React from "react"
import { BrowserRouter, Link } from "react-router-dom"
import { Box } from "@/components/ui"

function App({ routes }: { routes: React.ReactNode }) {
  return (
    <BrowserRouter>
      <Box
        fontFamily="sans"
        bg="gray-50"
        minH="screen"
        p={6}
        className="max-w-7xl mx-auto"
      >
        <Header />
        <main className="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Navigation */}
          <nav className="lg:col-span-1 space-y-2">
            <div className="space-y-1">
              <Link
                to="/"
                className="group flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
              >
                🦥 SlothTab
              </Link>
            </div>

            <ul className="space-y-1">
              <li>
                <Link
                  to="/dashboard"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  Dashboard
                </Link>
              </li>
              <li>
                <Link
                  to="/inbox"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  Inbox
                </Link>
              </li>
              <li>
                <Link
                  to="/activity"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  Activity
                </Link>
              </li>
              <li>
                <Link
                  to="/rules"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  Rules
                </Link>
              </li>
              <li>
                <Link
                  to="/settings"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium transition-colors hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                >
                  Settings
                </Link>
              </li>
              <li>
                <Link
                  to="/demo"
                  className="flex items-center rounded-md px-3 py-2 text-sm font-medium text-muted-foreground"
                >
                  Demo Mode
                </Link>
              </li>
            </ul>
          </nav>

          {/* Main content area */}
          <div className="lg:col-span-2">
            {routes}
          </div>
        </main>

        {/* Footer */}
        <footer className="mt-8 text-sm text-muted-foreground">
          <p>SlothTab • Local-first AI productivity agent</p>
        </footer>
      </Box>
    </BrowserRouter>
  )
}

export default App