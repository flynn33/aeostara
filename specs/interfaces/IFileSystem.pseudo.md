# IFileSystem Interface

Abstract filesystem operations used by adapters, backup, verification, and audit mechanics.

## Methods

### readFile(path) -> string

Read file content.

### writeFile(path, content)

Write file content.

### fileExists(path) -> Boolean

Check file presence.

### copyFile(fromPath, toPath) -> Boolean

Copy file content.

### appendFile(path, content)

Append content to file.
