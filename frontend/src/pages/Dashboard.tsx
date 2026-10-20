import React, { useEffect, useState } from "react"
import { Card, CardContent, Center, Heading, Text, Spinner, Badge } from "@/components/ui"
import { useParams } from "react-router-dom"

interface FileAnalysis {
  id: string
  filename: string
  action: "organized" | "renamed" | "summarized" | "needs_attention"
  destination?: string
  confidence: number
  summary?: string
  importance: "low" | "medium" | "high"
  timestamp: string
  reason: string
  tags: string[]
}

export default function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [files, setFiles] = useState<FileAnalysis[]>([])
  const [activity, setActivity] = useState<FileAnalysis[]>([])
  const [slothScore, setSlothScore] = useState({ organized: 0, renamed: 0, summarized: 0, duplicates: 0 })
  const [providerStatus, setProviderStatus] = useState("idle")

  // Simulate fetching from backend
  useEffect(() => {
    const mockFiles: FileAnalysis[] = [
      {
        id: "1",
        filename: "cloud-lab.pdf",
        action: "organized",
        destination: "College / Cloud Computing",
        confidence: 0.96,
        summary: "Instructions for creating and configuring a Google Cloud VM.",
        importance: "medium",
        timestamp: "2024-01-15T20:31:00Z",
        reason: "Cloud computing instructions detected.",
        tags: ["cloud-computing", "vm", "google-cloud"],
      },
      {
        id: "2",
        filename: "IMG_8273.png",
        action: "renamed",
        confidence: 0.94,
        summary: "Google Cloud console screenshot",
        importance: "medium",
        timestamp: "2024-01-15T20:29:00Z",
        reason: "Screenshot of cloud console detected.",
        tags: ["screenshot", "cloud-console"],
      },
      {
        id: "3",
        filename: "receipt_9281.jpg",
        action: "organized",
        destination: "Receipts",
        confidence: 0.92,
        summary: "Grocery receipt from 2024-01-10",
        importance: "low",
        timestamp: "2024-01-15T20:28:00Z",
        reason: "Receipt detected.",
        tags: ["receipt", "personal"],
      },
      {
        id: "4",
        filename: "assignment_final.docx",
        action: "organized",
        destination: "College / Assignments",
        confidence: 0.97,
        summary: "Final assignment for cloud computing course",
        importance: "high",
        timestamp: "2024-01-15T20:27:00Z",
        reason: "Assignment with upcoming deadline.",
        tags: ["assignment", "cloud-computing", "deadline"],
      },
    ]

    setFiles(mockFiles)
    setActivity(mockFiles.slice(0, 8))

    // Calculate sloth score
    const organized = mockFiles.filter(f => f.action === "organized").length
    const renamed = mockFiles.filter(f => f.action === "renamed").length
    const summarized = mockFiles.filter(f => f.tags.some(t => t === "summarized")).length
    setSlothScore({ organized, renamed, summarized, duplicates: 0 })
  }, [])

  return (
    <Card className="max-w-2xl mx-auto">
      <CardContent>
        <Heading size="2xl" mb={4} className="text-center">
          Good evening, Sloth. 🦥
        </Heading>

        <p className="text-muted-foreground mb-6 text-center">
          SlothTab handled{" "}
          {files.length}
          {" files."}
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6 justify-center">
          <div className="self-center">
            <Badge className="text-lg">{files.filter(f => f.action === "organized").length}</Badge>
            <Text className="text-xs mt-1 text-center">Organized</Text>
          </div>
          <div className="self-center">
            <Badge variant="secondary" className="text-lg">
              {files.filter(f => f.action === "renamed").length}
            </Badge>
            <Text className="text-xs mt-1 text-center">Renamed</Text>
          </div>
          <div className="self-center">
            <Badge variant="destructive" className="text-lg">
              {files.filter(f => f.tags.some(t => t === "summarized")).length}
            </Badge>
            <Text className="text-xs mt-1 text-center">Summarized</Text>
          </div>
          <div className="self-center">
            <Badge className="text-lg">{files.filter(f => f.action === "needs_attention").length}</Badge>
            <Text className="text-xs mt-1 text-center">Needs attention</Text>
          </div>
        </div>

        <div className="border-t border-border pt-6">
          <Heading size="xl" mb={4} className="text-center">
            Recent Activity
          </Heading>
          {activity.length === 0 && (
            <Text className="text-center text-muted-foreground">No activity yet. Select a folder to get started.</Text>
          )}
          <ul className="space-y-2 max-h-48 overflow-y-auto">
            {activity.map((file) => (
              <li
                key={file.id}
                className="flex items-start rounded-md p-2 transition-colors hover:bg-primary/5"
                aria-label={file.reason}
              >
                <div className="w-2 h-2 rounded-full bg-primary shrink-0 flex-shrink-0 mt-1"
                  style={{
                    backgroundColor: file.importance === "high"
                      ? "#ef4444"
                      : file.importance === "medium"
                      ? "#f59e0b"
                      : "#10b981",
                  }}
                />
                <div className="ml-3 flex-1 min-w-0">
                  <div className="font-medium truncate">{file.filename}</div>
                  <div className="text-xs text-muted-foreground">
                    {file.action === "organized"
                      ? `→ ${file.destination}`
                      : file.action === "renamed"
                      ? `→ ${file.filename}`
                      : file.action}
                  </div>
                  <div className="text-xs mt-1">
                    {file.timestamp}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-8 pt-8 border-t border-border">
          <Heading size="xl" mb={4} className="text-center">
            🦥 Sloth Score
          </Heading>
          <p className="text-3xl font-bold text-center">{files.length} files processed</p>
          <p className="text-sm text-muted-foreground text-center">
            Estimated time saved: ~{files.length * 3} minutes
          </p>
        </div>
      </CardContent>
    </Card>
  )
}