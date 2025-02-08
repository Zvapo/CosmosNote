"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ThemeToggle } from "./theme-toggle"

interface Message {
  role: "user" | "ai"
  content: string
}

export default function ResearchTool() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")

  const handleSend = () => {
    if (input.trim()) {
      setMessages([...messages, { role: "user", content: input }])
      // Placeholder for AI response
      setTimeout(() => {
        setMessages((prev) => [...prev, { role: "ai", content: `AI response to: ${input}` }])
      }, 1000)
      setInput("")
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <header className="border-b">
        <div className="container mx-auto px-4 flex items-center justify-between h-16">
          <h1 className="text-xl font-bold">Research Tool</h1>
          <ThemeToggle />
        </div>
      </header>

      <main className="flex-grow container mx-auto px-4 py-4">
        <Tabs defaultValue="chat" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="chat">Chat</TabsTrigger>
            <TabsTrigger value="map">Thought Map</TabsTrigger>
          </TabsList>

          <TabsContent value="chat" className="h-[calc(100vh-9rem)]">
            <div className="h-full flex flex-col">
              <ScrollArea className="flex-grow mb-4 border rounded-md p-4 !bg-[#fff0]">
                {messages.map((message, index) => (
                  <div key={index} className={`mb-4 flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div
                      className={`max-w-[80%] rounded-lg p-3 ${
                        message.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                      }`}
                    >
                      {message.content}
                    </div>
                  </div>
                ))}
              </ScrollArea>
              <div className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSend()}
                  placeholder="Ask a question..."
                  className="flex-grow"
                />
                <Button onClick={handleSend}>Send</Button>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="map" className="h-[calc(100vh-9rem)]">
            <div className="h-full border rounded-md overflow-hidden">
              <iframe id="quartz-iframe" src="http://localhost:8080" className="w-full h-full" title="Quartz Thought Map" />
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

