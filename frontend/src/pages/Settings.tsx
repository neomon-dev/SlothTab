import React, { useState } from "react"
import { Card, CardContent, Heading, Text, Button, Input, Select, Spinner } from "@/components/ui"

export default function Settings() {
  const [settings, setSettings] = useState({
    provider: "LM Studio" as "LM Studio" | "Ollama" | "Custom OpenAI-compatible",
    baseUrl: "http://localhost:1234/v1" as string,
    model: "gemma-2b" as string,
    apiKey: "" as string,
    minimumConfidence: 0.9 as number,
    autoMode: false as boolean,
    autoModeThreshold: 0.9 as number,
    duplicateDetection: true as boolean,
    generateSummary: true as boolean,
  })

  const [loading, setLoading] = useState(false)
  const [testResult, setTestResult] = useState<string | null>(null)

  const handleTestConnection = async () => {
    setLoading(true)
    setTestResult(null)

    // Simulate connection test
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // In a real app, this would test the actual connection
    setTestResult("✓ Connected\nModel: gemma-2b\nResponse time: 1.8 seconds")
    setLoading(false)
  }

  const handleSaveSettings = () => {
    // In a real app, this would save to backend
    // For now, just update local state
    setSettings((prev) => ({
      ...prev,
      minimumConfidence: Math.max(0, Math.min(1, prev.minimumConfidence)),
    }))
  }

  return (
    <Card>
      <CardContent>
        <Heading size="xl" mb={4}>
          Settings
        </Heading>

        {/* AI Provider Section */}
        <div className="mb-6">
          <Heading size="sm" mb={2}>
            AI Provider
          </Heading>

          <Select
            onValueChange={(val) => setSettings((s) => ({ ...s, provider: val }))}
            defaultValue={settings.provider}
          >
            <option value="LM Studio">LM Studio</option>
            <option value="Ollama">Ollama</option>
            <option value="Custom OpenAI-compatible">Custom OpenAI-compatible</option>
          </Select>

          {settings.provider === "LM Studio" && (
            <Input
              placeholder="http://localhost:1234/v1"
              value={settings.baseUrl}
              onChange={(e) =>
                setSettings((s) => ({ ...s, baseUrl: e.target.value }))
              }
            />
          )}

          {settings.provider === "Ollama" && (
            <Input
              placeholder="http://localhost:11434/v1"
              value={settings.baseUrl}
              onChange={(e) =>
                setSettings((s) => ({ ...s, baseUrl: e.target.value }))
              }
            />
          )}

          {settings.provider === "Custom OpenAI-compatible" && (
            <Input
              placeholder="https://api.openai.com/v1"
              value={settings.baseUrl}
              onChange={(e) =>
                setSettings((s) => ({ ...s, baseUrl: e.target.value }))
              }
            />
          )}

          <Input
            placeholder="Model (e.g., gemma-2b)"
            value={settings.model}
            onChange={(e) => setSettings((s) => ({ ...s, model: e.target.value }))}
          />

          {settings.apiKey && (
            <Input
              type="password"
              placeholder="API key (optional)"
              value={settings.apiKey}
              onChange={(e) =>
                setSettings((s) => ({ ...s, apiKey: e.target.value }))
              }
            />
          )}

          <Button onClick={handleTestConnection} disabled={loading}>
            {loading ? (
              <Spinner size="sm" />
            ) : (
              "Test Connection"
            )}
          </Button>

          {testResult && (
            <Text className="mt-2 text-sm text-success-foreground">
              {testResult}
            </Text>
          )}
        </div>

        {/* Processing Section */}
        <div className="mt-6">
          <Heading size="sm" mb={2}>
            Processing
          </Heading>

          <label className="flex items-center gap-2">
            <Input
              type="checkbox"
              checked={settings.autoMode}
              onChange={(e) =>
                setSettings((s) => ({ ...s, autoMode: e.target.checked }))
              }
            />
            <span>Auto Mode</span>
          </label>

          <label className="flex items-center gap-2 mt-2">
            <Input
              type="checkbox"
              checked={settings.duplicateDetection}
              onChange={(e) =>
                setSettings((s) => ({ ...s, duplicateDetection: e.target.checked }))
              }
            />
            <span>Duplicate Detection</span>
          </label>

          <label className="flex items-center gap-2 mt-2">
            <Input
              type="checkbox"
              checked={settings.generateSummary}
              onChange={(e) =>
                setSettings((s) => ({ ...s, generateSummary: e.target.checked }))
              }
            />
            <span>Generate Summary</span>
          </label>

          <label className="flex items-center gap-2 mt-2">
            <Input
              type="number"
              min={0}
              max={1}
              step={0.1}
              value={settings.minimumConfidence}
              onChange={(e) =>
                setSettings((s) => ({
                  ...s,
                  minimumConfidence: parseFloat(e.target.value),
                }))
              }
            />
            <span>Minimum Confidence {Math.round(
              settings.minimumConfidence * 100
            )}%</span>
          </label>
        </div>

        {/* Privacy Section */}
        <div className="mt-6 pt-6 border-t border-border">
          <Heading size="sm" mb={2}>
            🔒 LOCAL-FIRST
          </Heading>
          <Text>
            Your files stay on your machine. SlothTab sends AI requests only to the
            local model endpoint you configure. No cloud AI is required.
          </Text>
        </div>

        <Button
          className="mt-4 w-full"
          onClick={handleSaveSettings}
        >
          Save Settings
        </Button>
      </CardContent>
    </Card>
  )
}