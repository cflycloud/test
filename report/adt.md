```
token_func:[[name, line, val_type, [[name, line, val_type], [name, line, val_type]....]],
			[name, line, val_type, [[name, line, val_type], [name, line, val_type]....]]...... ]
token_val:[[name, line, val_type, [[name, line, val_type], [name, line, val_type]....]], 
           [name, line, val_type, [[name, line, val_type], [name, line, val_type]....]]......]
danger:[[filepath, line, function_name, risk, solve],
        [filepath, line, function_name, risk, solve].......]
invalidfunc:[[filepath, line, name], 
             [filepath, line, name]......]
invalidval:[[filepath, line, name],
            [filepath, line, name]......]
```

全为str

token list 中的最后一项可能为空。

```
token_func = [
    ["func1", 10, "int", [["var1", 12, "int"], ["var2", 14, "float"]]],
    ["func2", 20, "void", [["var3", 22, "char"], ["var4", 24, "double"]]],
    ["func3", 30, "int", [["var5", 32, "int"], ["var6", 34, "float"], ["var7", 36, "char"]]],
]

token_val = [
    ["var1", 50, "int", [["subvar1", 52, "int"], ["subvar2", 54, "float"]]],
    ["var2", 60, "float", [["subvar3", 62, "char"], ["subvar4", 64, "double"]]],
]

danger = [
    ["file1.c", 100, "func1", "Buffer Overflow", "Increase buffer size"],
    ["file2.c", 200, "func2", "Memory Leak", "Free allocated memory"],
    ["file3.c", 300, "func3", "Null Pointer Dereference", "Check for NULL before accessing pointer"],
]

invalidfunc = [
    ["file1.c", 150, "invalid_func1"],
    ["file2.c", 250, "invalid_func2"],
]

invalidval = [
    ["file1.c", 160, "invalid_var1"],
    ["file2.c", 260, "invalid_var2"],
]

```

