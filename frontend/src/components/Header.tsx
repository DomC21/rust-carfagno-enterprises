import { BarChart3 } from "lucide-react"

export function Header() {
  return (
    <header className="bg-black p-4 border-b border-[#FFD700]">
      <div className="container mx-auto flex items-center justify-between px-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="text-[#FFD700]" size={32} />
          <div>
            <h1 className="text-[#FFD700] text-2xl font-bold">Rust</h1>
            <p className="text-gray-400 text-sm">A Tool by Carfagno Enterprises</p>
          </div>
        </div>
      </div>
    </header>
  )
}
