import React, { useState } from "react"
import { Card, CardContent, Center, Heading, Text, Button, Spinner, Alert } from "@/components/ui"

export default function Inbox() {
  const [folderPath, setFolderPath] = useState<string>("")
  const [files, setFiles] = useState<any[]>([])
  const [analyzing, setAnalyzing] = useState(false)
  const [status, setStatus] = useState<string>("")

  const handleFolderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFolderPath(e.target.value)
  }

  const browseFolder = async () => {
    setAnalyzing(true)
    setStatus("")

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000))

    // Mock analysis results
    const mockFiles = [
      { name: "cloudnotes.txt", action: "organized", destination: "College / Notes" },
      { name: "receipt.jpg", action: "organized", destination: "Receipts" },
      { name: "screenshot.png", action: "renamed", suggested: "cloud-console-screenshot.png" },
    ]

    setFiles(mockFiles)
    setAnalyzing(false)
    setStatus(`✓ Analyzed 3 files`)
  }

  return (
    <Card className="max-w-2xl mx-auto">
      <CardContent>
        <Heading size="xl" mb={4} className="text-center">
          🦥 Your inbox is messy.
        </Heading>

        <p className="text-muted-foreground mb-6 text-center">
          Drop your files here and SlothTab will figure it out.
        </p>

        <div className="border rounded-md p-6 mb-6 justify-center" style={{ borderColor: "var(--border)" }}>
          <Center>
            <Button onClick={browseFolder} disabled={analyzing} className="w-full">
              {analyzing ? (
                <Spinner size="lg" />
              ) : (
                "Choose Folder"
              )}
            </Button>
          </Center>
        </div>

        {folderPath && (
          <Alert className="mb-4">
            <p>Folder: {folderPath}</p>
            {status && <p>{status}</p>}
          </Alert>
        )}

        {analyzing && (
          <div className="mt-4 justify-center">
            <Spinner size="lg" />
            <p>Analyzing files...</p>
          </div>
        )}

        {files.length > 0 && (
          <div className="mt-6 space-y-3">
            <Heading size="sm" mb={2} className="text-center">
              Pending Files
            </Heading>
            <ul className="space-y-2 max-h-48 overflow-y-auto">
              {files.map((file, i) => (
                <li
                  key={i}
                  className="flex items-center rounded-md p-2 transition-colors hover:bg-primary/5"
                  aria-label={file.name}
                >
                  <span className="w-10 h-10 rounded-md flex items-center justify-center shrink-0 bg-primary/10 text-primary mr-3">
                    {file.name?.slice(0, 2)}
                  </span>
                  <div className="flex-1 min-w-0">
                    <span className="font-medium">{file.name}</span>
                    {file.action && (
                      <span className="text-xs ml-2">
                        {file.action === "renamed"
                          ? `→ ${file.suggested}`
                          : file.action}
                      </span>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Empty state when no folder selected */}
        {!folderPath && files.length === 0 && (
          <Alert>
            <p className="text-center">
              🦥<br />
              Your inbox is messy.
            </p>
            <p className="text-center text-muted-foreground mt-2">
              Drop your files here and SlothTab will figure it out.
            </p>
            <p className="text-center mt-3">
              <Button onClick={() => setFolderPath("")} className="mt-2">
                Choose Folder
              </Button>
            </p>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}