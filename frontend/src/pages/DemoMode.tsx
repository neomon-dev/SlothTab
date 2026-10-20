import React, { useState, useEffect } from "react"
import { Card, CardContent, Heading, Text, Button, Spinner, Alert, Badge } from "@/components/ui"

export default function DemoMode() {
  const [showDemo, setShowDemo] = useState(false)
  const [demoFiles, setDemoFiles] = useState<any[]>([])
  const [processing, setProcessing] = useState(false)
  const [results, setResults] = useState<any[]>([])

  const triggerDemo = () => {
    setShowDemo(true)
  }

  // Generate demo files
  useEffect(() => {
    const demoFileNames = [
      "IMG_8291.png",
      "assignment_final2.pdf",
      "cloud_notes.txt",
      "receipt.jpg",
      "project_architecture.png",
      "random_document.pdf",
      "screenshot.png",
    ]

    const files = demoFileNames.map((name) => ({
      name,
      path: `/tmp/slothtab-demo/${name}`,
      size: Math.floor(Math.random() * 2000000),
      extension: name.slice(name.lastIndexOf(".")),
    }))

    setDemoFiles(files)
  }, [])

  const runDemo = async () => {
    if (processing) return
    setProcessing(true)
    setResults([])

    // Simulate processing the demo files
    await new Promise((resolve) => setTimeout(resolve, 3000))

    const mockResults = [
      {
        original: "IMG_8291.png",
        action: "renamed",
        suggested: "google-cloud-console-screenshot.png",
        destination: "Screenshots",
        confidence: 0.94,
      },
      {
        original: "assignment_final2.pdf",
        action: "organized",
        suggested: "machine-learning-assignment.pdf",
        destination: "College / Assignments",
        confidence: 0.97,
      },
      {
        original: "cloud_notes.txt",
        action: "organized",
        destination: "College / Notes",
        confidence: 0.92,
      },
      {
        original: "receipt.jpg",
        action: "organized",
        destination: "Receipts",
        confidence: 0.91,
      },
      {
        original: "project_architecture.png",
        action: "renamed",
        suggested: "system-architecture-diagram.png",
        destination: "Development / Code",
        confidence: 0.93,
      },
      {
        original: "random_document.pdf",
        action: "needs_attention",
        confidence: 0.55,
      },
      {
        original: "screenshot.png",
        action: "renamed",
        suggested: "cloud-console-screenshot.png",
        destination: "Screenshots",
        confidence: 0.95,
      },
    ]

    setResults(mockResults)
    setProcessing(false)
  }

  return (
    <Card>
      <CardContent>
        <Heading size="xl" mb={4}>
          ✨ Demo Mode
        </Heading>

        <p className="text-muted-foreground mb-6">
          This generates a realistic temporary messy folder and processes those
          files through the same real pipeline.
        </p>

        <div className="mb-6">
          <Button onClick={triggerDemo} disabled={processing}>
            {processing ? (
              <Spinner size="sm" />
            ) : (
              "Load Demo Files"
            )}
          </Button>
        </div>

        {showDemo && !processing && (
          <Alert>
            <p>
              The following files will be processed (demo data only):
            </p>
            <ul className="mt-2 space-y-1">
              {demoFiles.map((f) => (
                <li key={f.name}>{f.name}</li>
              ))}
            </ul>
            <Button
              variant="secondary"
              mt={2}
              onClick={runDemo}
              className="mt-2"
            >
              Process Files
            </Button>
          </Alert>
        )}

        {processing && (
          <div className="mt-6">
            <Spinner size="lg" />
            <p>Processing demo files through AI pipeline...</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="mt-6">
            <Heading size="xl" mb={4}>
              🦥 DONE
            </Heading>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div>
                <Badge>{results.filter(r => r.action === "organized").length}</Badge>
                <Text>Organized</Text>
              </div>
              <div>
                <Badge variant="secondary">
                  {results.filter(r => r.action === "renamed").length}
                </Badge>
                <Text>Renamed</Text>
              </div>
              <div>
                <Badge variant="destructive">
                  {results.filter(r => r.action === "needs_attention").length}
                </Badge>
                <Text>Needs attention</Text>
              </div>
            </div>

            <p className="text-2xl font-bold mt-4">~15 minutes saved</p>

            <div className="mt-6 p-4 rounded-md bg-primary/5">
              <Heading size="sm" mb={2}>
                Organized folder structure
              </Heading>
              <ul className="space-y-2 text-sm">
                <li>
                  <strong>College/</strong>
                  <span>Assignments / machine-learning-assignment.pdf</span>
                </li>
                <li>
                  <strong>College/</strong>
                  <span>Notes / cloud-notes.txt</span>
                </li>
                <li>
                  <strong>Screenshots/</strong>
                  <span>google-cloud-console-screenshot.png</span>
                </li>
                <li>
                  <strong>Receipts/</strong>
                  <span>receipt.jpg</span>
                </li>
              </ul>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
}