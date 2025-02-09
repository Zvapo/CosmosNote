export type Message = {
    role: "user" | "ai" | "tool"
    author?: string
    content?: string
    tool_name?: string
}