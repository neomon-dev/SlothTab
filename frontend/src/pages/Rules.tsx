import React, { useEffect, useState } from "react"
import { Card, CardContent, Heading, Text, Button, Input, Select, Alert } from "@/components/ui"

export default function Rules() {
  const [rules, setRules] = useState<any[]>([])
  const [newRuleName, setNewRuleName] = useState("")
  const [newRuleConditions, setNewRuleConditions] = useState("")
  const [newRuleActions, setNewRuleActions] = useState("")
  const [editingRule, setEditingRule] = useState<null | string>(null)

  // Simulate fetching from backend
  useEffect(() => {
    const mockRules = [
      {
        id: "1",
        name: "College priority",
        conditions: "Category = College AND Confidence > 90%",
        actions: "Move to: College/",
        enabled: true,
      },
      {
        id: "2",
        name: "Screenshot organizer",
        conditions: "File type = Image AND AI detects screenshot",
        actions: "Move to: Screenshots/",
        enabled: false,
      },
    ]
    setRules(mockRules)
  }, [])

  const handleCreateRule = () => {
    if (!newRuleName.trim()) return

    const newRule = {
      id: (Date.now()).toString(),
      name: newRuleName.trim(),
      conditions: newRuleConditions || "",
      actions: newRuleActions || "",
      enabled: true,
    }

    setRules([...rules, newRule])
    setNewRuleName("")
    setNewRuleConditions("")
    setNewRuleActions("")
  }

  const handleToggleRule = (id: string) => {
    setRules(
      rules.map((rule) =>
        rule.id === id ? { ...rule, enabled: !rule.enabled } : rule
      )
    )
  }

  const handleDeleteRule = (id: string) => {
    setRules(rules.filter((rule) => rule.id !== id))
  }

  return (
    <Card>
      <CardContent>
        <Heading size="xl" mb={4}>
          Rules
        </Heading>

        <div className="mb-6">
          <Input
            placeholder="Rule name"
            value={newRuleName}
            onChange={(e) => setNewRuleName(e.target.value)}
          />
          <Input
            placeholder="Conditions (e.g., Category = College)"
            value={newRuleConditions}
            onChange={(e) => setNewRuleConditions(e.target.value)}
          />
          <Input
            placeholder="Actions (e.g., Move to: College/)"
            value={newRuleActions}
            onChange={(e) => setNewRuleActions(e.target.value)}
          />
          <Button onClick={handleCreateRule}>Add Rule</Button>
        </div>

        <div className="space-y-3">
          {rules.map((rule) => (
            <div key={rule.id} className="p-3 rounded-md border border-border transition-colors hover:bg-primary/5">
              <div className="flex items-center justify-between mb-2">
                <Text size="sm" mb={0}>
                  {rule.name}
                </Text>
                {rule.enabled ? (
                  <Badge>Active</Badge>
                ) : (
                  <Badge variant="secondary">Inactive</Badge>
                )}
              </div>
              <div className="text-xs text-muted-foreground">
                <div>{rule.conditions || "No conditions"}</div>
                <div>{rule.actions || "No actions"}</div>
              </div>
              <div className="mt-2 flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setEditingRule(rule.id)}
                >
                  Edit
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDeleteRule(rule.id)}
                >
                  Delete
                </Button>
              </div>
            </div>
          ))}
        </div>

        {editingRule && (
          <Alert>
            <p>Editing rule: {editingRule}</p>
            <p>This feature would open a rule editor.</p>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}