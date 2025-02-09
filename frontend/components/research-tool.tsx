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
  const [response, setResponse] = useState<string>("")
  const [input, setInput] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)

  const socketUrl = process.env.NEXT_PUBLIC_SOCKET_URL || '';

  const {
    sendJsonMessage,
    lastJsonMessage,
  } = useWebSocket(socketUrl, {
    onOpen: () => console.log('opened'),
    //Will attempt to reconnect on all close events, such as server shutting down
    shouldReconnect: (closeEvent) => true,
  });

  useEffect(() => {
    if (lastJsonMessage) {
      const data = lastJsonMessage as { status: 'start_chat' | 'tool_called' | 'message' | 'complete', message: string, agent: string, tool_name?: string };

      if (data.status === "message") {
        setMessages(prev => {
          const currentMessage = prev[prev.length - 1];
          currentMessage.content = currentMessage.content + data.message;

          return [...prev.slice(0, -1), currentMessage];
        });

      } else if (data.status === "tool_called") {
        console.log("tool_called", data);
        setMessages(prev => [...prev, { role: "tool", tool_name: data.tool_name }]);
      } else if (data.status === "start_chat") {
        console.log("start_chat", data);
        setMessages(prev => [...prev, { role: "ai", content: data.message, author: data.agent }]);
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

