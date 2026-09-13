import { useContext } from 'react'
import { WorkspaceContext } from './workspace.context'

export function useWorkspace() {
  const context = useContext(WorkspaceContext)

  if (!context) {
    throw new Error(
      'useWorkspace debe utilizarse dentro de WorkspaceProvider.',
    )
  }

  return context
}
