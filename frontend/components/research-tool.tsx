"use client"

import useWebSocket, { ReadyState } from 'react-use-websocket';

import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ThemeToggle } from "./theme-toggle"
import { Message } from '@/lib/types';
import MessageComponent from './message-component';

export default function ResearchTool() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL || '';

  const {
    sendJsonMessage,
    lastJsonMessage,
  } = useWebSocket(socketUrl, {
    onOpen: () => console.log('opened'),
    //Will attempt to reconnect on all close events, such as server shutting down
    shouldReconnect: () => true,
  });

  useEffect(() => {
    if (lastJsonMessage) {
      const data = lastJsonMessage as { status: 'agent_message' | 'tool_message' | 'complete', message: string, agent: string, name?: string };

      console.log("data", data);

      if (data.status === "agent_message") {
        setMessages(prev => {
          return [...prev, { role: "ai", content: data.message }];
        });
      } else if (data.status === "tool_message") {
        setMessages(prev => [...prev, { role: "tool", message: data.message, tool_name: data.name }]);
      } else if (data.status === "complete") {
        setIsProcessing(false);
      }
    }
  }, [lastJsonMessage]);

  const handleSend = () => {
    if (input.trim()) {
      setIsProcessing(true);
      sendJsonMessage({
        user_prompt: input,
      });
      setMessages(prev => [...prev, { role: "user", content: input }]);
      setInput("");
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
                  <MessageComponent key={index} message={message} />
                ))}
                
                {isProcessing && (
                  <div className="loader" />
                )}
              </ScrollArea>
              
              <div className="flex gap-2">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSend()}
                  placeholder="Ask a question..."
                  className="flex-grow"
                />
                <Button onClick={handleSend} disabled={isProcessing}>Send</Button>
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

