export type Message = {
    role: "user" | "ai" | "tool"
    author?: string
    content?: string
    search_results?: SourceData[]
    tool_name?: string
}

export interface SourceData {
    url: string
    content: string
}