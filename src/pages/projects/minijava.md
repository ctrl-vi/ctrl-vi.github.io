---
article: 
    publishedTime: "2025-06-19T02:07:41-08:00"
    modifiedTime: "2025-06-19T02:07:41-08:00"
    authors: ["Violet Monserate", "Katherine Leavitt"]
    section: Class Projects
    tags: ["java", "c", "assembly", "gitlab"]
layout: '@components/MarkdownProjectLayout.astro'
title: Minijava Compiler 
description: Created a compiler (scanner, parser, codegen) from subset of Java to x86 assembly for CSE 401 
seoDescription: Violet Monserate and Katherine Leavitt created a compiler for a subset of Java, called MiniJava, as part of their CSE 401 class project. The compiler includes features such as arithmetic expressions, control flow, types, objects, dynamic dispatching, and a garbage collector. The project involved testing the compiler's functionality and ensuring compatibility between features. The team also added extra features like a garbage collector to manage memory efficiently. Overall, the project provided valuable experience in software architecture and object-oriented programming.
image:
    src: "@assets/minijava/minijava.png"
    alt: Collage of two different diagrams for the Minijava Compiler project. On the left is an Abstract Syntax Tree (AST) diagram, and on the right is a diagram of the garbage collector data structure. The AST diagram shows the structure of a line of code in the MiniJava language, with nodes representing different constructs, such as statements. The garbage collector diagram illustrates how objects are managed in memory, with a linked list of allocated objects and a roots list for tracking references.
startDate: '2025-9'
finishDate: '2025-12'
icons: ["java", "c", "assembly", "gitlab"]
---

![Collage of two different diagrams for the Minijava Compiler project. On the left is an Abstract Syntax Tree (AST) diagram, and on the right is a diagram of the garbage collector data structure. The AST diagram shows the structure of a line of code in the MiniJava language, with nodes representing different constructs, such as statements. The garbage collector diagram illustrates how objects are managed in memory, with a linked list of allocated objects and a roots list for tracking references.](@assets/minijava/minijava.png)

---
## Overview

As students in CSE 401 (Compilers) at UW, we were tasked with creating a compiler for a subset of Java, called MiniJava. The project involved implementing a scanner, parser, and code generator to translate MiniJava code into x86 assembly. We built the scanner with JFlex, the parser with Java CUP, and used an AST visitor architecture to keep each compiler pass modular.

## Minijava Compiler Features

Our code includes functionality for the MiniJava building blocks. We have functionality for:
- Minijava arithmetic expressions, which include plus, minus, and times on integers.
- Control flow, which provides for booleans, less than, and, or, not, if statements, and while loops.
- Types: integers, arrays (of ints), booleans, and classes. The main class has a public static void primary method, but every other method must return an integer or an object.
- Objects: Minijava objects can have fields and methods. The methods must return a value and can take parameters and contain their own local variables.
- Dynamic dispatching: classes can extend other classes and override methods. Methods that override other methods must have the same parameters and must return the same type or a subclass of the original return type.

## What We Wrote 

While I am not at liberty to share the code itself, here is a summary of what we wrote for each part of the compiler.

### JFlex Scanner
- Defined token rules for MiniJava keywords, identifiers, integer literals, operators, delimiters, and comments/whitespace.
- Routed lexical errors to readable compiler errors instead of failing silently.
- Tracked source locations (row/column) so later stages could report precise error positions.

### Java CUP Parser Grammar
- Wrote grammar productions for classes, methods, statements, expressions, arrays, and inheritance-related syntax.
- Added precedence/associativity declarations for operators (for example, arithmetic and boolean operators) so expressions parse as intended.
- Tailor the grammar to avoid shift/reduce conflicts and reduce ambiguity, especially in expression parsing.
- Used CUP semantic actions to construct AST nodes during parsing.

### AST Node Hierarchy
- Implemented node classes representing programs, classes, methods, variable declarations, statements (if/while/assign/print), and expressions (math, boolean, method calls, field access, array operations, object creation, etc.).
- Stored source metadata (line/column) in nodes to improve semantic and runtime error diagnostics.

### Visitor Pattern Compiler Passes
- Used visitor interfaces and concrete visitor implementations to traverse AST nodes without embedding every pass directly in node classes.
- Kept the pipeline separated by responsibility: symbol/type analysis visitors, checking/validation visitors, and code generation visitors.
- This made it easier to add features (like garbage collection hooks and null checks) without rewriting the entire AST structure.

### Semantic Analysis Infrastructure
- Built and checked class/method/field environments and scope-aware variable lookup.
- Enforced MiniJava type rules, including inheritance-aware method overriding and subtype-compatible returns.
- Validated method calls, assignments, control-flow conditions, and array usage.

### Code Generation and Runtime

- Emitted x86-64 assembly for expressions, control flow, object allocation, method dispatch (vtable-based), and arrays.
- Added runtime checks (including null dereference checks in key dereference paths).
- Integrated generated code with `boot.c` and custom garbage-collector support routines (`mark`/`sweep`) through direct calls from emitted assembly.

## Testing overview

While working on every part of the project, we simply tested the outputs on small example files. We traced what the compiler ought to do by hand (e.g., writing out the scanner tokens, drawing the AST, writing specific examples of bad semantics). These files were then translated into proper test cases. To perform this validation for the initial parts of our project (scanner, parser, and semantics), we utilized the MiniJavaTestBuilder class and junit suite provided by the staff.

To test the codegen, we created test files with expected outputs, ran them through an online Java compiler to verify the intended output (including checking which statements Java doesn’t accept) against the runtime of the program our compiler. To ensure coverage of a variety of test cases, both team members independently wrote test cases targeting each of the different codegen “milestones” we needed to achieve: integer expressions, object creation and method calls, variables/parameters, control flow/booleans, classes (including inheritance), and arrays. We also tested the provided sample programs.

We ensured that later tests would also implement features from prior sections to maintain compatibility between features (e.g., HardArray.java uses integer math, variables/parameters, and control flow in addition to all the array features). Additionally, since code generation is the last step and calls all prior parts (scanning, parsing, and semantic testing), these tests also test all previous parts. In fact, we uncovered (and subsequently resolved) an error in our semantics section during codegen testing related to dynamic dispatch!

## Extra feature: Garbage Collector (!!!!!) 

We also added a prominent feature: a garbage collector that frees unused objects. The “mark and sweep” procedure runs at the exit of any method, and at the exit of the program, including at runtime errors. The “sweep” procedure ensures that all objects are freed.

We maintain a linked list of all allocated objects in the program. For each object, we add a boolean flag indicating whether it is still in use. To understand which of the fields of a given object to “mark,” we also store a pointer to “ObjectStructure” inside of the vtable.

There is also an object that lists all the parameters and fields for a given scope, and this is tracked through a “roots list.” The last node for the roots list is a reference to the global scope.  The following diagram details the garbage collector’s data structures.

![The garbage collector diagram illustrates how objects are managed in memory, with a linked list of allocated objects and a roots list for tracking references.](@assets/minijava/garbage-collector.png)
*Fig. 1: Garbage Collector Data Structures*

At the end of a scope (method call/main function), we “mark.” Starting at all of the root nodes, we follow all of the pointers, which indicate that the given reference is used, and mark the object’s “in-use” flag. We recursively continue the process on the fields of the given object. 

After marking, we then “sweep”; sweeping involves traversing the linked list of allocated objects. All of the objects that are “marked” are clearly referenced somewhere and could still be effective, and thus are not freed. Objects that are not marked are therefore not useful, as they are never referenced and thus “orphaned,” allowing us to free it back to the allocator. 

In the case of the program terminating (whether by runtime error or exiting normally), we must free all of the objects that may still be remaining, which can be done by simply calling sweep without marking, which acts as though NONE of the objects are referenced and thus not in use and able to be swept and disposed of.

Note that this does decrease the speed of the final program, because we implemented a stop-the-world, blocking the program during the marking and sweeping processes so that no new objects are created, changing the state of the the roots list or the allocated objects lists.

All of the above procedures are bundled with boot.c. During runtime, the compiled program itself maintains the underlying data structure and then calls the “mark” and “sweep” procedures as necessary with a standard “callq” instruction.

## Other Features

To support richer debugging and error handling, we also stored additional information within our AST nodes: the row and column that the node starts at. This is especially evident during semantic passes, where we use a helper function to provide a consistent template for generating errors that includes the error location.

We added some checks for null pointer dereferencing. When we allocate space for an object, we use the mjcalloc function given to us, which sets the memory at the specified location to 0. When we dereference a pointer, we check whether it is 0, because that indicates an object that was declared but not initialized.

We tried to set up the CSE Virtual Image but ran into some issues, so we decided to transfer our compiled code to attu to test. We wrote and used the handy-dandy build-and-transfer script that compiles, builds, and transfers the output file to attu (under Violet’s account), and we had attu open in a second terminal to run the output there. 

We wanted to add support for arrays of objects, not just ints, but we didn’t quite get to that. However, some places use arrays where we tried to avoid hardcoding int type in, so that in the future we could add support for other types. One example of this is our ArrayType class in ADT/Types for our semantics part of the project: a field stores elementType, and we could use that for other element types besides integers. 

## Work Was Indeed Divided

We wrote most of the code together using IntelliJ's Code With Me. We talked over the general structure together, using material we learned in class. Coding concurrently allowed us to work faster, talk through anywhere we got stuck, and do code review to change style conventions, catch bugs, and ensure consistency.

## Conclusion 

We had a lot of fun with this project, although at times it was frustrating :) It was so rewarding when the pieces finally clicked or when you squashed the bug causing infinite loops and consistent segfaults (there was a bug that would cause a segfault ONLY when running with valgrind, which was highly annoying to squash). We learned a lot and got to practice writing code (and test cases) in Java, C, and assembly, debugging with gdb, x86-64, checking grammars, and examining associativity. 

The overall freedom in the project was intimidating but really allowed us to make large-scale choices about software architecture and to implement proper object-oriented programming conventions. 

As we mentioned before, the next thing we would like to add is support for arrays of objects that aren’t ints. That kind of change would require rewriting a little bit of every section of the code from scanning/parsing to codegen, and we didn’t get to it.
