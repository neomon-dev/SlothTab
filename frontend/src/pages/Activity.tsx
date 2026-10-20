import React, { useEffect, useState } from "react"
import { Card, CardContent, Heading, Text, Button, Badge, Spinner } from "@/components/ui"

export default function Activity() {
  const [filter, setFilter] = useState<string>("all")
  const [loading, setLoading] = useState(true)
  const [activities, setActivities] = useState<any[]>([])

  // Simulate fetching from backend
  useEffect(() => {
    const mockActivities = [
      {
        id: "1",
        filename: "cloud-lab.pdf",
        operation: "organized",
        old_path: "Downloads/cloud-lab.pdf",
        new_path: "College/Cloud Computing/cloud-lab.pdf",
        timestamp: "2024-01-15T20:31:00Z",
      },
      {
        id: "2",
        filename: "IMG_8273.png",
        operation: "renamed",
        old_path: "Downloads/IMG_8273.png",
        new_path: "Screenshots/cloud-console-screenshot.png",
        timestamp: "2024-01-15T20:29:00Z",
      },
      {
        id: "3",
        filename: "receipt_9281.jpg",
        operation: "organized",
        old_path: "Downloads/receipt_9281.jpg",
        new_path: "Receipts/receipt_9281.jpg",
        timestamp: "2024-01-15T20:28:00Z",
      },
      {
        id: "4",
        filename: "assignment_final.docx",
        operation: "organized",
        old_path: "Downloads/assignment_final.docx",
        new_path: "College/Assignments/assignment_final.docx",
        timestamp: "2024-01-15T20:27:00Z",
      },
      {
        id: "5",
        filename: "unknown_document.pdf",
        operation: "needs_review",
        old_path: "Downloads/unknown_document.pdf",
        new_path: "Downloads/unknown_document.pdf",
        timestamp: "2024-01-15T20:25:00Z",
      },
    ]

    setActivities(mockActivities)
    setLoading(false)
  }, [filter])

  const filteredActivities = filter === "all"
    ? activities
    : activities.filter(a => a.operation === filter)

  return (
    <Card className="max-w-2xl mx-auto">
      <CardContent>
        <Heading size="xl" mb={4} className="text-center">
          Activity
        </Heading>

        <div className="mb-4 justify-center">
          <Button
            variant="outline"
            onClick={() => setFilter("all")}
            className={filter === "all" ? "border-primary" : ""}
            aria-label="Show all activities"
          >
            All
          </Button>
          <Button
            variant="outline"
            onClick={() => setFilter("organized")}
            className={filter === "organized" ? "border-primary" : ""}
            aria-label="Show organized activities"
          >
            Organized
          </Button>
          <Button
            variant="outline"
            onClick={() => setFilter("renamed")}
            className={filter === "renamed" ? "border-primary" : ""}
            aria-label="Show renamed activities"
          >
            Renamed
          </Button>
          <Button
            variant="outline"
            onClick={() => setFilter("summarized")}
            className={filter === "summarized" ? "border-primary" : ""}
            aria-label="Show summarized activities"
          >
            Summarized
          </Button>
          <Button
            variant="outline"
            onClick={() => setFilter("needs_review")}
            className={filter === "needs_review" ? "border-primary" : ""}
            aria-label="Show needs review activities"
          >
            Needs Review
          </Button>
        </div>

        {loading && (
          <div className="flex justify-center py-8">
            <Spinner aria-label="Loading activity feed" />
            <span className="ms-2">Loading...</span>
          </div>
        )}

        {!loading && activities.length === 0 && (
          <div className="text-center py-8">
            <Text>No activities found.</Text>
          </div>
        )}

        <ul
          role="list"
          className="space-y-2 max-h-64 overflow-y-auto"
          aria-label="Activity history"
        >
          {filteredActivities.map((a) => (
            <li
              key={a.id}
              role="listitem"
              className="flex items-start rounded-md p-2 transition-colors hover:bg-primary/5"
              aria-label={a.filename}
            >
              <div
                role="presentation"
                className="w-2 h-2 rounded-full shrink-0 flex-shrink-0 mt-1"
                style={{
                  backgroundColor: a.operation === "organized"
                    ? "#10b981"
                    : a.operation === "renamed"
                    ? "#f59e0b"
                    : a.operation === "summarized"
                    ? "#3b82f6"
                    : "#6b7280",
                }}
              />
              <div className="ml-3 flex-1 min-w-0">
                <div role="presentation" className="font-medium">{a.filename}</div>
                <div role="presentation" className="text-xs text-muted-foreground">
                  {a.timestamp}
                </div>
                {a.old_path && (
                  <div role="presentation" className="text-xs ml-1">
                    {a.operation === "organized"
                      ? `→ ${a.new_path}`
                      : a.operation === "renamed"
                      ? `→ ${a.new_path.split('/').pop()}`
                      : a.operation}
                  </div>
                )}
              </div>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}